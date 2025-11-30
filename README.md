

---

#  **Backend README (FastAPI + MongoDB Todo API)**  


A secure and modular backend built using **FastAPI**, **MongoDB**, and **JWT Authentication** to support the Todo React Native App.

---

##  Features

- User Signup & Login (JWT-based)
- Protected routes using Bearer Tokens
- Create Todos
- Get User-specific Todos
- Toggle Todo Completion
- MongoDB Database
- Clean response models using Pydantic

---

##  Project Structure

Backend/
├── main.py
├── auth.py
├── database.py
├── schemas.py
├── models.py (optional)
├── requirements.txt

## 🛠 Setup Instructions

### 1️ Install dependencies

```bash
pip install -r requirements.txt

2 Start FastAPI server
uvicorn main:app --reload

3 MongoDB Setup

Local MongoDB

MongoDB Atlas
Update the connection string in database.py.


API Endpoints (CURL Included)
🔹 Signup
curl -X POST http://127.0.0.1:8000/auth/signup \
-H "Content-Type: application/json" \
-d '{"email": "test@gmail.com", "password": "123456"}'

🔹 Login (Returns Token)
curl -X POST http://127.0.0.1:8000/auth/login \
-H "Content-Type: application/json" \
-d '{"email": "test@gmail.com", "password": "123456"}'


Response:

{
  "token": "your.jwt.token.here"
}

🔹 Get Profile
curl -X GET http://127.0.0.1:8000/auth/me \
-H "Authorization: Bearer <TOKEN>"

🔹 Create Todo
curl -X POST http://127.0.0.1:8000/todos \
-H "Authorization: Bearer <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"title": "Buy milk"}'

🔹 Get Todos (User-specific)
curl -X GET http://127.0.0.1:8000/todos \
-H "Authorization: Bearer <TOKEN>"

🔹 Toggle Todo
curl -X PATCH http://127.0.0.1:8000/todos/<TODO_ID>/toggle \
-H "Authorization: Bearer <TOKEN>"
