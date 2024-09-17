from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import task_crud
from app.crud.tag import tag_crud
from app.models import Task, User


async def check_name_duplicate_for_task(
        task_name: str,
        session: AsyncSession,
        user: User
) -> None:
    """Проверка на совпадение имени в БД."""
    task_id = await task_crud.get_task_id_by_name(
        task_name, session, user
    )
    if task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_name_duplicate_for_tag(
        tag_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на совпадение имени в БД."""
    tag_id = await tag_crud.get_tag_id_by_name(
        tag_name, session
    )
    if tag_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_task_exists(
        task_id: int,
        session: AsyncSession,
        user: User
) -> Task:
    """Проверка на существование задачи в БД."""
    task = await task_crud.get(
        task_id, session, user
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Задача не найдена!'
        )
    return task


async def check_valid_name_for_task(obj_in):
    """Валидация имени."""
    if (
        obj_in.name is None or len(obj_in.name) > 100 or
        not obj_in.name.strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Не подходящее имя для проекта!"
        )
