from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task, User, Tag


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
            session: AsyncSession,
            user: User
    ):
        """Обновление данных объекта."""
        if db_obj.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this task"
            )

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
        user: User
    ):
        """Удаление объекта."""
        if db_obj.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to delete this task"
            )
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_tasks_by_tag(
        tag: str,
        session: AsyncSession,
        user: User
    ) -> list[Task]:
        """Получение задач по тегу."""
        result = await session.execute(
            select(Task).join(Task.tags).where(
                Tag.title == tag,
                Task.user_id == user.id
            )
        )
        return result.scalars().all()

    async def get_task_id_by_name(
        self,
        task_name: str,
        session: AsyncSession,
        user: User
    ) -> Optional[int]:
        """Получение объекта по имени."""
        db_task_id = await session.execute(
            select(Task.id).where(
                Task.name == task_name,
                Task.user_id == user.id
            )
        )
        return db_task_id.scalars().first()


task_crud = CRUDTask(Task)
