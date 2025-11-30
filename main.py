from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from typing import List, Optional
from bson import ObjectId
from database import db
from schemas import UserCreate, UserLogin, TodoCreate, TodoResponse
from auth import create_access_token, verify_token
from datetime import datetime

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Allow mobile apps / emulator to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- AUTH ----------
@app.post("/auth/signup")
async def signup(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    await db.users.insert_one({"email": user.email, "password": hashed_password})
    return {"message": "Signup successful"}


@app.post("/auth/login")
async def login(user: UserLogin):
    existing = await db.users.find_one({"email": user.email})
    if not existing or not pwd_context.verify(user.password, existing["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"email": user.email})
    return {"token": token}


# ---------- Dependency to get current user email from Authorization header ----------
async def get_current_user_email(Authorization: Optional[str] = Header(None)) -> str:
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    parts = Authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = parts[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return email


# ---------- GET CURRENT USER ----------
@app.get("/auth/me")
async def me(user_email: str = Depends(get_current_user_email)):
    user = await db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user["email"]}


# ---------- TODOS ----------
@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, user_email: str = Depends(get_current_user_email)):
    todo_doc = {
        "title": todo.title,
        "completed": False,
        "user_email": user_email,
        "timestamp": datetime.utcnow()
    }
    res = await db.todos.insert_one(todo_doc)
    return {
        "id": str(res.inserted_id),
        "title": todo_doc["title"],
        "completed": todo_doc["completed"],
        "user_email": todo_doc["user_email"],
        "timestamp": todo_doc["timestamp"]
    }


@app.get("/todos", response_model=List[TodoResponse])
async def get_todos(user_email: str = Depends(get_current_user_email)):
    todos = await db.todos.find({"user_email": user_email}).to_list(100)
    out = []
    for t in todos:
        out.append({
            "id": str(t["_id"]),
            "title": t.get("title"),
            "completed": t.get("completed", False),
            "user_email": t.get("user_email"),
            "timestamp": t.get("timestamp")
        })
    return out


@app.patch("/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo(todo_id: str, user_email: str = Depends(get_current_user_email)):
    todo = await db.todos.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.get("user_email") != user_email:
        raise HTTPException(status_code=403, detail="Not allowed")
    new_status = not todo.get("completed", False)
    await db.todos.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": new_status}})
    updated = await db.todos.find_one({"_id": ObjectId(todo_id)})
    return {
        "id": str(updated["_id"]),
        "title": updated.get("title"),
        "completed": updated.get("completed"),
        "user_email": updated.get("user_email"),
        "timestamp": updated.get("timestamp")
    }
