#Фоновые задачи в FastAPI
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# Параметры Cookie
from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}

# Доступ к файлам cookie

from fastapi import FastAPI, Cookie

app = FastAPI()


@app.get("/")
def root(last_visit=Cookie()):
    return {"last visit": last_visit}

# Установка файлов cookie
from fastapi import FastAPI, Response
from datetime import datetime

app = FastAPI()

@app.get("/")
def root(response: Response):
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")  # получаем текущую дату и время
    response.set_cookie(key="last_visit", value=now)
    return {"message": "куки установлены"}

# Прочие возможности при работе с cookie
@router.post("/logout", status_code=204)
async def logout_user(response: Response):
    response.delete_cookie("example_access_token")

# Заголовки запросов
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# Повторяющиеся заголовки
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
"""
X-Token: foo
X-Token: bar
Ответ был бы таким:

{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
"""
# Доступ к заголовкам запросов
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/")
def root(user_agent: str = Header()):
    return {"User-Agent": user_agent}


from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
def root():
    data = "Hello from here"
    return Response(content=data, media_type="text/plain", headers={"Secret-Code": "123459"})

@app.get("/")
def root(response: Response):
    response.headers["Secret-Code"] = "123459"
    return {"message": "Hello from my api"}

# Чтобы реализовать базовую аутентификацию в FastAPI, нам необходимо выполнить следующие действия:

# Шаг 1: Импорт зависимостей
from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Шаг 2: Создайте приложение FastAPI и экземпляр HTTPBasic
app = FastAPI()
security = HTTPBasic()
# Шаг 3: Создайте модель пользователя

class User(BaseModel):
    username: str
    password: str

# добавим симуляцию базы данных в виде массива объектов юзеров
USER_DATA = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]

# Шаг 4: Определите функцию аутентификации
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

# Шаг 5: Задайте логику получения информации о пользователе и его пароле
# симуляционный пример
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None
# Шаг 6: Защитите конечные точки с помощью аутентификации

@app.get("/protected_resource/")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}