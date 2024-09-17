from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Tag


class CRUDTag:
    """Класс для CRUD операции Tag."""

    def __init__(self, model):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession
    ) -> list[Tag]:
        """Получение нескольких объектов из БД."""
        db_objs = await session.execute(
            select(self.model)
        )
        return db_objs.scalars().all()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Tag:
        """Получение объекта их БД по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ) -> Tag:
        """
        Создание объекта в БД.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_tag_id_by_name(
        self,
        tag_title: str,
        session: AsyncSession,
    ) -> Optional[Tag]:
        """Получение объекта по имени."""
        db_tag = await session.execute(
            select(Tag).where(
                Tag.title == tag_title
            )
        )
        return db_tag.scalars().first()


tag_crud = CRUDTag(Tag)
