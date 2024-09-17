from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.models.user import User

router = APIRouter()


@router.post("/auth/telegram")
async def link_telegram_account(
    telegram_username: str,
    email: str,
    session: AsyncSession = Depends(get_async_session),
):
    user = await session.get(User, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.telegram_username = telegram_username
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "Telegram account linked successfully"}
