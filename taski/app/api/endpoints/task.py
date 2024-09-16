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
    check_name_duplicate, check_project_exists,
    check_valid_name_for_project,
    check_valid_description_for_project
)
from app.core.user import current_superuser, current_user

router = APIRouter()


@router.post(
    '/',
    response_model=TaskDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_task(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Создание объекта Task с валидацией входных данных.
    """
    await check_valid_name_for_project(task)
    await check_name_duplicate(task.name, session)
    new_task = await task_crud.create(task, session, user)
    session.refresh(new_task)
    return new_task


@router.get(
    '/{my}',
    response_model=list[TaskDB],
    response_model_exclude_none=True,
)
async def get_all_tasks(
    session: AsyncSession = Depends(get_async_session),
    my: User = Depends(current_user)
):
    """
    Получение всех объектов Task.
    """
    task_from_db = await task_crud.get_multi(session, user=my)
    if task_from_db is None:
        raise HTTPException(
            status_code=404,
            detail='Задач пока нету.'
        )
    return task_from_db


@router.patch(
    '/{task_id}',
    response_model=TaskDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_task(
        task_id: int,
        obj_in: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
        my: User = Depends(current_user),
):
    """
    Частичное обновление данных для Task c валидацией.
    """
    task = await check_project_exists(task_id, session, my)

    if obj_in.name is not None:
        await check_valid_name_for_project(obj_in)
        await check_name_duplicate(obj_in.name, session)
    await check_valid_description_for_project(obj_in)

    task = await task_crud.update(task, obj_in, session, my)
    return task


@router.delete(
    '/{task_id}',
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
        my: User = Depends(current_user),
):
    """
    Удаление объекта Task.
    """
    task = await check_project_exists(task_id, session, my)
    task = await task_crud.remove(task, session, my)
    return task
