from fastapi import APIRouter, Path, Body, HTTPException, status, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, delete
from app.database.connection import get_session
from app.models.tasks import Task, TaskList
from app.models.users import User
from app.routes.users import get_current_user

task_router = APIRouter(tags=["Tasks"])
templates = Jinja2Templates(directory="templates")


# -------------------- HTML-страницы --------------------

@task_router.get("/")
@task_router.get("/tasks")
async def show_tasks(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": tasks, "todo": None, "user": current_user},
    )


@task_router.post("/tasks")
async def create_task_from_form(
    title: str = Form(...),
    description: str = Form(""),
    task_status: str = Form("Новая"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    new_task = Task(
        title=title.strip(),
        description=description.strip(),
        status=task_status,
        user_id=current_user.id, 
    )
    session.add(new_task)
    session.commit()
    return RedirectResponse(url="/tasks", status_code=303)


@task_router.get("/tasks/{task_id}")
async def show_single_task(
    request: Request,
    task_id: int = Path(..., title="ID задачи"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или нет прав доступа.")

    all_tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todo": task, "todos": all_tasks, "user": current_user},
    )


@task_router.post("/tasks/{task_id}/delete")
async def delete_task_from_form(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или нет прав доступа.")

    session.delete(task)
    session.commit()
    return RedirectResponse(url="/tasks", status_code=303)


# -------------------- REST API --------------------

@task_router.post("/task", status_code=status.HTTP_201_CREATED)
async def add_task(
    task: Task = Body(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    task.id = None  # Генерация ID поручается базе данных
    task.user_id = current_user.id  # Устанавливаем владельца
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": "Задача добавлена.", "id": task.id}


@task_router.get("/task", response_model=TaskList)
async def retrieve_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return {"tasks": tasks}


@task_router.get("/task/{task_id}", response_model=Task)
async def get_single_task(
    task_id: int = Path(..., title="ID задачи"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена или нет прав доступа.",
        )
    return task


@task_router.put("/task/{task_id}")
async def update_task(
    task_id: int = Path(..., title="ID задачи"),
    task_data: Task = Body(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена или нет прав доступа.",
        )

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": "Задача обновлена.", "task": task}


@task_router.delete("/task/{task_id}")
async def remove_task(
    task_id: int = Path(..., title="ID задачи"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена или нет прав доступа.",
        )
    session.delete(task)
    session.commit()
    return {"message": "Задача удалена"}


@task_router.delete("/task")
async def remove_all_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> dict:
    statement = delete(Task).where(Task.user_id == current_user.id)
    session.exec(statement)
    session.commit()
    return {"message": "Все ваши задачи удалены"}