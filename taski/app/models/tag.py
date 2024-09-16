from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.orm import relationship


from app.core.db import Base


class Tag(Base):
    """
    Модель таблицы тэгов.
    """
    task = relationship('Task')
    title = Column(String(100), unique=True, nullable=False)
