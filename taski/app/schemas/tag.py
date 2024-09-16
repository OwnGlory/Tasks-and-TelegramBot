from typing import Optional
from datetime import datetime

from pydantic import (
    BaseModel, Field, Extra, PositiveInt
)


class TagBase(BaseModel):
    """Базовая схема для тэгов."""
    title: str

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                "title": "Важное",

            }
        }


class TagCreate(TagBase):
    """Схема для созданий пожертвований."""
    pass


class TagAllDB(TagBase):
    """
    Схема для вывода информации при создании пожертвования
    и получении пожертвований пользователя.
    """
    id: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class TagDB(TagBase):
    """Схема для получения всех пожертвований."""
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
