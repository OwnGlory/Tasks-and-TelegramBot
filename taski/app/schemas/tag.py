from typing import Optional

from pydantic import (
    BaseModel, Extra
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

    class Config:
        orm_mode = True


class TagDB(TagBase):
    """Схема для получения всех пожертвований."""

    class Config:
        orm_mode = True
