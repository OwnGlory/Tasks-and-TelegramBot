from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_projects_crud
from app.crud.investions import DataBaseWork
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.api.validators import (
    check_name_duplicate, check_project_exists,
    check_project_open, check_project_full_amount,
    check_project_invested_amount, check_valid_name_for_project,
    check_valid_full_amount_for_project, check_valid_description_for_project
)
from app.services.investions import invest_in_project
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создание объекта CharityProject с валидацией входных данных.
    """
    data_base_work = DataBaseWork(session)
    await check_valid_name_for_project(charity_project)
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_projects_crud.create(charity_project, session)
    await invest_in_project(new_project, data_base_work)
    session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получение всех объектов CharityProject.
    """
    projects_from_db = await charity_projects_crud.get_multi(session)
    return projects_from_db


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Частичное обновление данных для CharityProject c валидацией.
    """
    charity_project = await check_project_exists(
        project_id, session
    )

    await check_project_open(charity_project)
    await check_project_full_amount(obj_in, charity_project)
    if obj_in.name is not None:
        await check_valid_name_for_project(obj_in)
        await check_name_duplicate(obj_in.name, session)
    await check_valid_full_amount_for_project(obj_in)
    await check_valid_description_for_project(obj_in)

    charity_project = await charity_projects_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Удаление объекта CharityProject.
    """
    charity_project = await check_project_exists(
        project_id, session
    )
    await check_project_invested_amount(charity_project)
    charity_project = await charity_projects_crud.remove(
        charity_project, session
    )
    return charity_project
