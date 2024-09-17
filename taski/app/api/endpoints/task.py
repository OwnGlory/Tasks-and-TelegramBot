from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.task import task_crud
from app.models import User
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskDB,
)
from app.api.validators import (
    check_name_duplicate_for_task, check_task_exists,
    check_valid_name_for_task,
)
from app.core.user import current_user

router = APIRouter()


@router.post(
    '/',
    response_model=TaskDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_new_task(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Создание объекта Task с валидацией входных данных.
    """
    await check_valid_name_for_task(task)
    await check_name_duplicate_for_task(task.name, session, user)
    new_task = await task_crud.create(task, session, user)
    await session.refresh(new_task)
    return new_task


@router.get(
    '/',
    response_model=list[TaskDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получение всех объектов Task.
    """
    task_from_db = await task_crud.get_multi(session, user)
    if task_from_db is None:
        raise HTTPException(
            status_code=404,
            detail='Задач пока нету.'
        )
    return task_from_db


@router.get(
    '/{task_id}',
    response_model=TaskDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получение объекта Task."""
    await check_task_exists(task_id, session, user)
    task_from_db = await task_crud.get(task_id, session, user)
    if task_from_db is None:
        raise HTTPException(
            status_code=404,
            detail='Задач пока нету.'
        )
    return task_from_db


@router.get(
    '/by_tag/{tag}',
    response_model=list[TaskDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_tasks_by_tag(
    tag: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получение задач по тегу.
    """
    tasks = await task_crud.get_tasks_by_tag(tag, session, user)
    if not tasks:
        raise HTTPException(
            status_code=404,
            detail='Задачи с таким тегом не найдены.'
        )
    return tasks


@router.patch(
    '/{task_id}',
    response_model=TaskDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def partially_update_task(
        task_id: int,
        obj_in: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Частичное обновление данных для Task c валидацией.
    """
    task = await check_task_exists(task_id, session, user)

    if obj_in.name is not None:
        await check_valid_name_for_task(obj_in)
        await check_name_duplicate_for_task(obj_in.name, session)

    task = await task_crud.update(task, obj_in, session, user)
    return task


@router.delete(
    '/{task_id}',
    dependencies=[Depends(current_user)]
)
async def remove_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Удаление объекта Task.
    """
    task = await check_task_exists(task_id, session, user)
    task = await task_crud.remove(task, session, user)
    return task
