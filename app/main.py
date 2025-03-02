from fastapi import FastAPI, Form
from app.models.models import UserCreate

app = FastAPI()

users = []
@app.post("/create_user")
async def create_user(user: UserCreate):
    users.append(user)
    return user
