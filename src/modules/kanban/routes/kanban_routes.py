from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.kanban.schemas.kanban import KanbanBoardResponse
from src.modules.kanban.services.kanban_service import KanbanService
from src.modules.users.schemas.user import UserResponse
from src.shared.base.schemas import ErrorResponse
from src.shared.exceptions.domain import DomainException
from src.shared.middleware.dependencies import get_current_active_user, get_kanban_service

router = APIRouter(prefix="/kanban", tags=["Tablero Kanban"])


@router.get(
    "/{project_id}",
    response_model=KanbanBoardResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Obtener tablero Kanban de un proyecto",
)
async def get_kanban_board(
    project_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    kanban_service: Annotated[KanbanService, Depends(get_kanban_service)],
) -> KanbanBoardResponse:
    try:
        return await kanban_service.get_board(project_id)
    except DomainException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
