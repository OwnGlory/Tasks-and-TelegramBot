from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field, Extra

from app.schemas.tag import TagDB


class TaskBase(BaseModel):
    """Базовый класс для схем задачи."""
    name: Optional[str]
    description: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "name": "5",
                "description": "Проект для пожертвований",
                "tags": ["Важное"]
            }
        }


class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название задачи',
        description='Уникальное названние задачи'
    )
    description: str = Field(..., min_length=2)
    tags: Optional[List[str]] = Field(None, title='Список тегов')


class TaskUpdate(TaskBase):
    """Схема для обновления задачи."""
    user_id: int


class TaskDB(TaskBase):
    """Схема для вывода информации о задаче."""
    id: Optional[int] = Field(0)
    create_date: Optional[datetime]
    update_date: Optional[datetime]
    tags: Optional[List[str]]

    class Config:
        orm_mode = True
