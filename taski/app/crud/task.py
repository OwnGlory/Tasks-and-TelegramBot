from typing import Optional
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.models import CharityProject
from app.crud.base import CRUDBase


def format_timediff(timediff: timedelta) -> str:
    total_seconds = int(timediff.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, microseconds = divmod(remainder, 1)
    return f"{days} days, {hours}:{minutes}:{seconds}.{microseconds:06d}"


class CRUDCharityProject(CRUDBase):
    """Класс для CRUD операций CharityProject."""

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Получение объекта их БД по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
    ):
        """Создание объекта в БД."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        """Обновление данных объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Получение объекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_all_close_project(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str, str]]:
        difference_stmt = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        )
        close_projects = await session.execute(
            select([CharityProject])
            .where(CharityProject.fully_invested == 1,)
            .order_by(difference_stmt)
        )
        close_projects = close_projects.scalars().all()
        projects_list = [
            {
                'name': project.name,
                'duration': format_timediff(
                    project.close_date - project.create_date
                ),
                'description': project.description
            }
            for project in close_projects
        ]
        print(projects_list)
        return projects_list


charity_projects_crud = CRUDCharityProject(CharityProject)
