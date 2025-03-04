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