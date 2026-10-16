from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


class TaskList(BaseModel):
    tasks: list[Task]
