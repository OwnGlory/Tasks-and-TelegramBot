from datetime import timedelta, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.models import Task, User, Tag


def format_timediff(timediff: timedelta) -> str:
    total_seconds = int(timediff.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, microseconds = divmod(remainder, 1)
    return f"{days} days, {hours}:{minutes}:{seconds}.{microseconds:06d}"


class CRUDTask:
    """Класс для CRUD операций Task."""

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession,
            user: User
    ):
        """Получение нескольких объектов из БД."""
        db_objs = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return db_objs.scalars().all()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
            user: User
    ):
        """Получение объекта их БД по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
                self.model.user_id == user.id
            )
        )
        return db_obj.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        """Создание объекта в БД."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        """Обновление данных объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_tasks_by_tag(
        tag: str,
        session: AsyncSession
    ) -> list[Task]:
        """Получение задач по тегу."""
        result = await session.execute(
            select(Task).join(Task.tags).where(Tag.title == tag)
        )
        return result.scalars().all()


task_crud = CRUDTask(Task)
