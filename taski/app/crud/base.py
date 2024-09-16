from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс для CRUD операций."""

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Получение нескольких объектов из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
