from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str


USER_DATA = [User(**{"username": "user1", "password": "pass1"}),
             User(**{"username": "user2", "password": "pass2"})]

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
            )
    return user

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None
@app.get("/login")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



