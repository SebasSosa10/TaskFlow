from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.tasks.schemas.task import TaskResponse
from src.modules.tasks.services.task_service import TaskService
from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import (
    UserCreate,
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
    UserUpdate,
)
from src.modules.users.services.user_service import UserService
from src.shared.base.schemas import ErrorResponse, MessageResponse, PaginatedResponse
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    DomainException,
    ForbiddenError,
)
from src.shared.middleware.dependencies import (
    get_current_active_user,
    get_task_service,
    get_user_service,
    require_roles,
)

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    summary="Crear usuario",
)
async def create_user(
    data: UserCreate,
    current_user: Annotated[
        UserResponse, Depends(require_roles(UserRole.ADMINISTRADOR))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    try:
        return await user_service.create_user(data, current_user.id, current_user.role)
    except (AlreadyExistsError, ForbiddenError) as exc:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(exc, AlreadyExistsError)
            else status.HTTP_403_FORBIDDEN
        )
        raise HTTPException(status_code=status_code, detail=exc.message) from exc


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
)
async def list_users(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[UserResponse]:
    users, total = await user_service.get_users(skip=skip, limit=limit)
    return PaginatedResponse(items=users, total=total, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Obtener usuario por ID",
)
async def get_user(
    user_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    try:
        return await user_service.get_user(user_id)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    summary="Actualizar usuario",
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: Annotated[
        UserResponse, Depends(require_roles(UserRole.ADMINISTRADOR))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    try:
        return await user_service.update_user(
            user_id, data, current_user.id, current_user.role
        )
    except AlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.message
        ) from exc
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Eliminar usuario",
)
async def delete_user(
    user_id: int,
    current_user: Annotated[
        UserResponse, Depends(require_roles(UserRole.ADMINISTRADOR))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> MessageResponse:
    try:
        await user_service.delete_user(user_id, current_user.id, current_user.role)
        return MessageResponse(message="Usuario eliminado correctamente")
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Actualizar rol de usuario",
)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    current_user: Annotated[
        UserResponse, Depends(require_roles(UserRole.ADMINISTRADOR))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    try:
        return await user_service.update_user_role(
            user_id, data, current_user.id, current_user.role
        )
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Activar o desactivar usuario",
)
async def update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    current_user: Annotated[
        UserResponse, Depends(require_roles(UserRole.ADMINISTRADOR))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    try:
        return await user_service.update_user_status(
            user_id, data, current_user.id, current_user.role
        )
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.get(
    "/{user_id}/tasks",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Listar tareas asignadas a un usuario",
)
async def list_user_tasks(
    user_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[TaskResponse]:
    try:
        tasks, total = await task_service.get_tasks_by_user(
            user_id, skip=skip, limit=limit
        )
        return PaginatedResponse(items=tasks, total=total, skip=skip, limit=limit)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc
