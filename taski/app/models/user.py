# app/models/user.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    String
)

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель для таблицы Пользователи."""
    task = relationship('Task')
    telegram_username = Column(String(150), unique=True, nullable=True)
