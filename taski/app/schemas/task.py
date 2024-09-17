from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, Extra


class TaskBase(BaseModel):
    """Базовый класс для схем задачи."""
    name: Optional[str]
    description: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "name": "Первый проект",
                "description": "Проект для пожертвований",
                "create_date": "15.09.2024"
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
    user_id: int


class TaskUpdate(TaskBase):
    """Схема для обновления задачи."""
    user_id: int


class TaskDB(BaseModel):
    """Схема для вывода информации о задаче."""
    id: Optional[int] = Field(0)
    create_date: Optional[datetime]
    update_date: Optional[datetime]

    class Config:
        orm_mode = True
