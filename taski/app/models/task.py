from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
    DateTime
)

from app.core.db import Base


class CharityProject(Base):
    """
    Модель таблицы задач.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(String(100), ForeignKey('tag.id'))
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    update_date = Column(DateTime)

    def __repr__(self):
        return (
            f'Проект {self.name}'
        )
