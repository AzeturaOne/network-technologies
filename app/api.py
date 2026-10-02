from fastapi import FastAPI
from app.task import task_router
app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return { "message": "Hello World"}

app.include_router(task_router)
