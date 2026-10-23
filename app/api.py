import uvicorn
from fastapi import FastAPI
from app.routes.tasks import task_router
from app.routes.users import user_router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Task Planner Application")
app.add_middleware(SessionMiddleware, secret_key="super-secret-practice-key")

app.include_router(user_router, prefix="/user")
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=80, reload=True)