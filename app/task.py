from fastapi import APIRouter, Path, Body, HTTPException, status
from app.model import Task, TaskList

task_router = APIRouter()

task_list = []

@task_router.post("/task", status_code=201)
async def add_task(task: Task) -> dict:
    task_list.append(task)
    return {"message": "Задача добавлена."}

@task_router.get("/task", response_model=TaskList)
async def retrieve_tasks() -> dict:
    return {"tasks": task_list}

@task_router.get("/task/{task_id}", response_model=Task)
async def get_single_task(task_id: int = Path(..., title="ID задачи которую мы хотим получить.")) -> dict:
    for task in task_list:
        if task.id == task_id:
            return task
    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
detail="Задача с таким ID не существует.",
)

@task_router.put("/task/{task_id}")
async def update_task(task_id: int = Path(..., title="ID задачи, которую мы хотим обновить."), task: Task = Body(..., title="Новые данные задачи.")) -> dict:
    for i, existing in enumerate(task_list):
        if existing.id == task_id:
            task_list[i] = task
            return {"message": "Задача обновлена.", "task": task}
    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
detail="Задача с таким ID не существует.",
)


@task_router.delete("/task/{task_id}")
async def remove_task(task_id: int = Path(..., title="ID задачи которую мы хотим удалить.")) -> dict:
    for i, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(i)
            return {"message": "Задача удалена"}
    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
detail="Задача с таким ID не существует.",
)

@task_router.delete("/task")
async def remove_all_tasks() -> dict:
    task_list.clear()
    return {"message": "Все задачи удалены"}