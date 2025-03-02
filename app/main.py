from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("../templates/index.html")
    # return {"message": "Hello World"}


@app.post("/calc/{num1}/{num2}")
async def calculate(num1, num2) -> float:
    try:
        num1 = float(num1)
    except ValueError:
        return {ValueError: f"Value must be numeric"}
    try:
        num2 = float(num2)
    except ValueError:
        return {ValueError: f"Value must be numeric"}
    sum: float = num1 + num2
    return {"result": sum}

@app.post('/calculate')
async def calculate(num1: float, num2: float):
    return {f'sum of numbers {num1} and {num2} is ': f'{num1+num2}'}