from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tag import (
    TagCreate,
    TagDB,
    TagAllDB,
)

from app.api.validators import check_name_duplicate_for_tag
from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.tag import tag_crud


router = APIRouter()


@router.post(
    '/',
    response_model=TagAllDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_tag(
        tag: TagCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание объекта Tag."""
    await check_name_duplicate_for_tag(tag.title, session)
    new_tag = await tag_crud.create(tag, session)
    return new_tag


@router.get(
    '/{Tag_id}',
    response_model=TagDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получение всех объектов Donation."""
    task_from_db = await tag_crud.get(task_id, session)
    if task_from_db is None:
        raise HTTPException(
            status_code=404,
            detail='Тэгов пока нету.'
        )
    return task_from_db


@router.get(
    '/{tags}',
    response_model=list[TagDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение всех объектов Task.
    """
    task_from_db = await tag_crud.get_multi(session)
    if task_from_db is None:
        raise HTTPException(
            status_code=404,
            detail='Задач пока нету.'
        )
    return task_from_db


@router.patch(
    '/{tag_id}',
    dependencies=[Depends(current_user)]
)
async def update_tag(
        session: AsyncSession = Depends(get_async_session),
):
    """Метод для запрета обновления тэгов."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Нельзя изменять тэги!'
    )


@router.delete(
    '/{tag_id}',
    dependencies=[Depends(current_user)]
)
async def delete_tag(
        session: AsyncSession = Depends(get_async_session),
):
    """Метод для запрета удаления тэгов."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Нельзя удалять тэги!'
    )
