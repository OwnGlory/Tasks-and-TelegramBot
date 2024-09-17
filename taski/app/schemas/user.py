from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для получения информации о пользователе."""
    telegram_username: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользоваеля."""
    telegram_username: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""
    telegram_username: Optional[str]
