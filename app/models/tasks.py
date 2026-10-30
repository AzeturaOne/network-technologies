from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.models.users import User


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: str

    # Внешний ключ на таблицу users
    user_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True),
    )

    # Двусторонняя связь с User
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"back_populates": "tasks"}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Починить МФУ HP LaserJet Pro MFP M28w",
                "description": "МФУ перестало печатать, хотя сканирует и копирует. Требуется диагностика и ремонт.",
                "status": "В работе",
            }
        }
    )


class TaskList(BaseModel):
    tasks: list[Task]
