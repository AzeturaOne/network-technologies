from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView

from app.models.users import User
from app.models.tasks import Task

# Разрешаем взаимные типы
Task.model_rebuild(_types_namespace={"User": User})
User.model_rebuild(_types_namespace={"Task": Task})

from app.database.connection import engine_url, conn
from app.routes.tasks import task_router
from app.routes.users import user_router

app = FastAPI(title="Task Planner")

app.add_middleware(SessionMiddleware, secret_key="super-secret-session-key")

app.include_router(user_router)
app.include_router(task_router)


class TaskAdmin(ModelView, model=Task):
    column_list = ["id", "title", "status", "user_id"]
    column_searchable_list = ["title", "description"]
    name = "Задача"
    name_plural = "Задачи"
    icon = "fa-solid fa-list-check"


class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "username"]
    column_searchable_list = ["email", "username"]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


admin = Admin(app, engine_url, title="Панель управления")
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)


@app.on_event("startup")
def on_startup():
    conn()
