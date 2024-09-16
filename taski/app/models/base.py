from sqlalchemy import Column, Table, ForeignKey

from app.core.db import Base


task_tag = Table(
    'task_tag', Base.metadata,
    Column('task_id', ForeignKey('task.id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id'), primary_key=True)
)
