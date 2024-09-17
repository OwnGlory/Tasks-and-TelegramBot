from fastapi import APIRouter

from app.api.endpoints import (
    task_router,
    tag_router,
    user_router
)

main_router = APIRouter()
main_router.include_router(
    task_router, prefix='/task',
    tags=['Task']
)
main_router.include_router(
    tag_router, prefix='/tag',
    tags=['Tag']
)

main_router.include_router(user_router)
