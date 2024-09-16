from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationAllDB,
)

from app.core.user import current_superuser, current_user
from app.models import User
from app.core.db import get_async_session
from app.crud.donation import donation_crud

router = APIRouter()


@router.post(
    '/',
    response_model=DonationAllDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создание объекта Donation - пожертвования."""
    data_base_work = DataBaseWork(session)
    new_donation = await donation_crud.create(donation, session, user)
    await invest_donation(new_donation, data_base_work)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donation_info(
    session: AsyncSession = Depends(get_async_session)
):
    """Получение всех объектов Donation."""
    donation_from_db = await donation_crud.get_multi(session)
    return donation_from_db


@router.get(
    '/{my}',
    response_model=list[DonationAllDB],
)
async def get_user_donation_info(
        session: AsyncSession = Depends(get_async_session),
        my: User = Depends(current_user)
):
    """Получение всех пожертвований пользователя."""
    user_donation = await donation_crud.get_donations_by_user(
        session=session, user=my
    )
    if user_donation is None:
        raise HTTPException(
            status_code=404,
            detail='Пожертвований пока нету.'
        )
    return user_donation


@router.patch(
    '/{donation_id}'
)
async def update_donation(
        session: AsyncSession = Depends(get_async_session),
):
    """Метод для запрета обновления пожертвований."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Нельзя изменять пожертвования!'
    )


@router.delete(
    '/{donation_id}'
)
async def delete_donation(
        session: AsyncSession = Depends(get_async_session),
):
    """Метод для запрета удаления пожертвований."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Нельзя удалять пожертвования!'
    )
