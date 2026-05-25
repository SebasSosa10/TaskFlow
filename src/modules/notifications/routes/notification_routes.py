from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.notifications.schemas.notification import NotificationCreate, NotificationResponse
from src.modules.notifications.services.notification_service import NotificationService
from src.modules.users.schemas.user import UserResponse
from src.shared.base.schemas import ErrorResponse, PaginatedResponse
from src.shared.exceptions.domain import DomainException, ForbiddenError
from src.shared.middleware.dependencies import get_current_active_user, get_notification_service

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get(
    "",
    response_model=PaginatedResponse[NotificationResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar notificaciones del usuario autenticado",
)
async def list_notifications(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[NotificationResponse]:
    notifications, total = await notification_service.get_notifications(
        current_user.id, skip=skip, limit=limit
    )
    return PaginatedResponse(items=notifications, total=total, skip=skip, limit=limit)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Crear notificación",
)
async def create_notification(
    data: NotificationCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    notification_service: Annotated[NotificationService, Depends(get_notification_service)],
) -> NotificationResponse:
    try:
        return await notification_service.create_notification(
            data, current_user.id, current_user.role
        )
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except DomainException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
