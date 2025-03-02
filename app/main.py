from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Feedback(BaseModel):
    name: str
    message: str | None = None

feedbacks = list()

# Пример пользовательских данных (для демонстрационных целей)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}
@app.post("/feedback")
async def get_feedback(fb: Feedback):
    feedbacks.append(fb)
    return {
    "message": f"Feedback received. Thank you, {fb.name}!"
}
# Конечная точка для получения информации о пользователе по ID
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}

@app.get("/users/")
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])
