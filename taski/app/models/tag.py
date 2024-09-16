from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import relationship


from .base import Base, task_tag


class Tag(Base):
    """
    Модель таблицы тэгов.
    """
    title = Column(String(100), unique=True, nullable=False)
    tasks = relationship("Task", secondary=task_tag, back_populates='tags')
