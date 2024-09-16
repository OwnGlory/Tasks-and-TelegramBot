from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_projects_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка на совпадение имени в БД."""
    project_id = await charity_projects_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка на существование проекта в БД."""
    charity_project = await charity_projects_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Переговорка не найдена!'
        )
    return charity_project


async def check_project_open(charity_project):
    """Проверка на состояние проекта(открыт или закрыт)."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя редактировать закрытый проект!"
        )


async def check_project_invested_amount(charity_project):
    """Проверка на наличие внесенных средств."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!"
        )


async def check_project_full_amount(obj_in, charity_project):
    """Проверяется меньше ли требуемая сумма уже внесенной."""
    if (
        obj_in.full_amount and
        obj_in.full_amount < charity_project.invested_amount
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Требуемая сумма не может быть меньше уже вложенной!"
        )


async def check_valid_name_for_project(obj_in):
    """Валидация имени."""
    if (
        obj_in.name is None or len(obj_in.name) > 100 or
        not obj_in.name.strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Не подходящее имя для проекта!"
        )


async def check_valid_full_amount_for_project(obj_in):
    """Валидация требуемой суммы."""
    if obj_in.full_amount is not None and obj_in.full_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Цель фонда должна быть больше нуля!"
        )


async def check_valid_description_for_project(obj_in):
    """Валидация описания проекта."""
    if obj_in.description is not None and not obj_in.description.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Описание не может быть пустым!"
        )
