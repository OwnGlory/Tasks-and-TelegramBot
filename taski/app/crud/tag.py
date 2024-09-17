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
    ):
        """Получение нескольких объектов из БД."""
        db_objs = await session.execute(
            select(self.model)
        )
        return db_objs.scalars().all()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Получение объекта их БД по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ):
        """
        Создание объекта в БД.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


tag_crud = CRUDTag(Tag)
