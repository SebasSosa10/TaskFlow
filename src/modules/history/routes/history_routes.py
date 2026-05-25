from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.history.schemas.history import HistoryResponse
from src.modules.history.services.history_service import HistoryService
from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import UserResponse
from src.shared.base.schemas import ErrorResponse, PaginatedResponse
from src.shared.exceptions.domain import DomainException
from src.shared.middleware.dependencies import (
    get_current_active_user,
    get_history_service,
    require_roles,
)

router = APIRouter(prefix="/history", tags=["Historial"])


@router.get(
    "",
    response_model=PaginatedResponse[HistoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar historial de actividades",
)
async def list_history(
    _: Annotated[
        UserResponse,
        Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.LIDER_PROYECTO)),
    ],
    history_service: Annotated[HistoryService, Depends(get_history_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[HistoryResponse]:
    entries, total = await history_service.get_history(skip=skip, limit=limit)
    return PaginatedResponse(items=entries, total=total, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=PaginatedResponse[HistoryResponse],
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Historial de actividades por usuario",
)
async def list_history_by_user(
    user_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    history_service: Annotated[HistoryService, Depends(get_history_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[HistoryResponse]:
    try:
        entries, total = await history_service.get_history_by_user(
            user_id, skip=skip, limit=limit
        )
        return PaginatedResponse(items=entries, total=total, skip=skip, limit=limit)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc
