from fastapi import APIRouter, Path, Body
from app.model import Task

task_router = APIRouter()

task_list = []

@task_router.post("/task")
async def add_task(task: Task) -> dict:
    task_list.append(task)
    return {"message": "Задача добавлена."}

@task_router.get("/task")
async def retrieve_tasks() -> dict:
    return {"tasks": task_list}

@task_router.get("/task/{task_id}")
async def get_single_task(task_id: int = Path(..., title="ID задачи которую мы хотим получить.")) -> dict:
    for task in task_list:
        if task.id == task_id:
            return { "task": task }
    return { "message": "Задачи с таким ID не существует." }

@task_router.put("/task/{task_id}")
async def update_task(task_id: int = Path(..., title="ID задачи, которую мы хотим обновить."), task: Task = Body(..., title="Новые данные задачи.")) -> dict:
    for i, existing in enumerate(task_list):
        if existing.id == task_id:
            task_list[i] = task
            return {"message": "Задача обновлена.", "task": task}
            
    return {"message": "Задача с таким ID не найдена."}


@task_router.delete("/task/{task_id}")
async def remove_task(task_id: int = Path(..., title="ID задачи которую мы хотим удалить.")) -> dict:
    for i, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(i)
            return {"message": "Задача удалена"}
    return {"message": "Задачи с таким ID не существует."}

