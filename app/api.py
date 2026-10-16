from fastapi import FastAPI
from app.task import task_router

app = FastAPI(title="Task Application")
app.include_router(task_router)
