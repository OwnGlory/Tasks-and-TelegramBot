from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для получения информации о пользователе."""
    telegram_username: str


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользоваеля."""
    telegram_username: str


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""
    telegram_username: str
