from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """Класс для CRUD операции Donation."""

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        """
        Создание объекта в БД и проверка на сущестование пользователя.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_donations_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        """Получение пожертвований пользователя."""
        db_user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
