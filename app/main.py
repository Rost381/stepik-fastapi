from fastapi import FastAPI, Response, Cookie
from pydantic import BaseModel
from uuid import uuid4
import uvicorn

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

sessions = dict()

user_db = {
    "admin": User(username="admin", password="admin"),
    "user123": User(username="user123", password="password123")
}

@app.post("/login")
async def login(user: User, response: Response) -> dict:
    db_user = user_db.get(user.username)
    if db_user and user.password == db_user.password:
        session_token = str(uuid4())
        sessions[user.username] = session_token
        response.set_cookie(key="session_token", value=session_token, secure=True, httponly=True)
        return {"session_token": session_token}

    return {"message": "Invalid username or password"}

@app.get("/user")
async def get_user(session_token = Cookie(None)) -> dict:
    for key, val in sessions.items():
        if val == session_token:
            return {"username": key}
    return {"message": "Invalid session token"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



