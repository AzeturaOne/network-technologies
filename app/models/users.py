from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr, ConfigDict

if TYPE_CHECKING:
    from app.models.tasks import Task


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    username: Optional[str] = None

    tasks: List["Task"] = Relationship(
        sa_relationship_kwargs={
            "back_populates": "user",
            "cascade": "all, delete-orphan",
        }
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "azetura_one@uust.ru",
                "username": "azetura_one",
            }
        }
    )


class NewUser(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
