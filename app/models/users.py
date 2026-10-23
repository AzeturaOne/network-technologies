from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.tasks import Task


class User(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    tasks: Optional[list[Task]] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "azetura_one@uust.ru",
                "username": "azetura_one",
                "tasks": [],
            }
        }
    )


class NewUser(User):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "azetura_one@uust.ru",
                "password": "The_best_password_ever_123_!@#",
                "username": "azetura_one",
                "tasks": [],
            }
        }
    )


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "azetura_one@uust.ru",
                "password": "The_best_password_ever_123_!@#",
            }
        }
    )