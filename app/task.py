from fastapi import APIRouter, Path, Body, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.model import Task, TaskList

task_router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Хранение в памяти, как в исходном проекте.
task_list: list[Task] = []


# -------------------- HTML-страницы --------------------

@task_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": task_list, "todo": None},
    )


@task_router.get("/tasks")
async def show_tasks(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": task_list, "todo": None},
    )


@task_router.post("/tasks")
async def create_task_from_form(
    title: str = Form(...),
    description: str = Form(""),
    task_status: str = Form("Новая"),
):
    next_id = max((task.id for task in task_list), default=0) + 1
    task_list.append(
        Task(
            id=next_id,
            title=title.strip(),
            description=description.strip(),
            status=task_status,
        )
    )
    return RedirectResponse(url="/tasks", status_code=303)


@task_router.get("/tasks/{task_id}")
async def show_single_task(request: Request, task_id: int = Path(..., title="ID задачи")):
    for task in task_list:
        if task.id == task_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"todo": task, "todos": task_list},
            )
    raise HTTPException(status_code=404, detail="Задача с таким ID не существует.")


@task_router.get("/tasks/{task_id}/edit")
async def edit_task_page(request: Request, task_id: int):
    for task in task_list:
        if task.id == task_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"edit_task": task, "todos": task_list, "todo": None},
            )
    raise HTTPException(status_code=404, detail="Задача с таким ID не существует.")


@task_router.post("/tasks/{task_id}/edit")
async def update_task_from_form(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    task_status: str = Form("Новая"),
):
    for index, task in enumerate(task_list):
        if task.id == task_id:
            task_list[index] = Task(
                id=task_id,
                title=title.strip(),
                description=description.strip(),
                status=task_status,
            )
            return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)
    raise HTTPException(status_code=404, detail="Задача с таким ID не существует.")


@task_router.post("/tasks/{task_id}/delete")
async def delete_task_from_form(task_id: int):
    for index, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(index)
            return RedirectResponse(url="/tasks", status_code=303)
    raise HTTPException(status_code=404, detail="Задача с таким ID не существует.")


# -------------------- Существующий REST API --------------------

@task_router.post("/task", status_code=201)
async def add_task(task: Task) -> dict:
    if any(existing.id == task.id for existing in task_list):
        raise HTTPException(status_code=409, detail="Задача с таким ID уже существует.")
    task_list.append(task)
    return {"message": "Задача добавлена."}


@task_router.get("/task", response_model=TaskList)
async def retrieve_tasks() -> dict:
    return {"tasks": task_list}


@task_router.get("/task/{task_id}", response_model=Task)
async def get_single_task(task_id: int = Path(..., title="ID задачи которую мы хотим получить.")):
    for task in task_list:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Задача с таким ID не существует.")


@task_router.put("/task/{task_id}")
async def update_task(
    task_id: int = Path(..., title="ID задачи, которую мы хотим обновить."),
    task: Task = Body(..., title="Новые данные задачи."),
) -> dict:
    for i, existing in enumerate(task_list):
        if existing.id == task_id:
            if task.id != task_id:
                raise HTTPException(status_code=400, detail="ID задачи в URL и теле запроса должны совпадать.")
            task_list[i] = task
            return {"message": "Задача обновлена.", "task": task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Задача с таким ID не существует.")


@task_router.delete("/task/{task_id}")
async def remove_task(task_id: int = Path(..., title="ID задачи которую мы хотим удалить.")) -> dict:
    for i, task in enumerate(task_list):
        if task.id == task_id:
            task_list.pop(i)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Задача с таким ID не существует.")


@task_router.delete("/task")
async def remove_all_tasks() -> dict:
    task_list.clear()
    return {"message": "Все задачи удалены"}
