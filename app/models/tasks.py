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
    user_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True),
    )

    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"back_populates": "tasks"}
    )