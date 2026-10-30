import os
from sqlmodel import SQLModel, Session, create_engine

from app.models.users import User
from app.models.tasks import Task

DATA_DIR = os.getenv("DATA_DIR", "/project/data")
os.makedirs(DATA_DIR, exist_ok=True)

database_file = os.path.join(DATA_DIR, "tasks.db")
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}

engine_url = create_engine(
    database_connection_string,
    echo=True,
    connect_args=connect_args
)


def conn():
    SQLModel.metadata.create_all(engine_url)


def get_session():
    with Session(engine_url) as session:
        yield session