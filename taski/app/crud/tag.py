from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag


class CRUDTag:
    """Класс для CRUD операции Tag."""

    def __init__(self, model):
        self.model = model

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


donation_crud = CRUDTag(Tag)
