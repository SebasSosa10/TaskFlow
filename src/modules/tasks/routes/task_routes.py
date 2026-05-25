from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.schemas.task import (
    TaskAssignUpdate,
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.modules.tasks.services.task_service import TaskService
from src.modules.users.schemas.user import UserResponse
from src.shared.base.schemas import ErrorResponse, MessageResponse, PaginatedResponse
from src.shared.exceptions.domain import (
    BusinessRuleError,
    DomainException,
    ForbiddenError,
)
from src.shared.middleware.dependencies import get_current_active_user, get_task_service

router = APIRouter(prefix="/tasks", tags=["Tareas"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Crear tarea",
)
async def create_task(
    data: TaskCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    try:
        return await task_service.create_task(data, current_user.id, current_user.role)
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.get(
    "",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar tareas",
)
async def list_tasks(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[TaskResponse]:
    tasks, total = await task_service.get_tasks(skip=skip, limit=limit)
    return PaginatedResponse(items=tasks, total=total, skip=skip, limit=limit)


@router.get(
    "/status/{status}",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar tareas por estado",
)
async def list_tasks_by_status(
    status: TaskStatus,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[TaskResponse]:
    tasks, total = await task_service.get_tasks_by_status(
        status, skip=skip, limit=limit
    )
    return PaginatedResponse(items=tasks, total=total, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Obtener tarea por ID",
)
async def get_task(
    task_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    try:
        return await task_service.get_task(task_id)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    summary="Actualizar tarea",
)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    try:
        return await task_service.update_task(
            task_id, data, current_user.id, current_user.role
        )
    except BusinessRuleError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message
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
    "/{task_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Eliminar tarea",
)
async def delete_task(
    task_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> MessageResponse:
    try:
        await task_service.delete_task(task_id, current_user.id, current_user.role)
        return MessageResponse(message="Tarea eliminada correctamente")
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    summary="Actualizar estado de tarea",
)
async def update_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    try:
        return await task_service.update_status(
            task_id, data, current_user.id, current_user.role
        )
    except BusinessRuleError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message
        ) from exc
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.patch(
    "/{task_id}/assign",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Asignar tarea a usuario",
)
async def assign_task(
    task_id: int,
    data: TaskAssignUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskResponse:
    try:
        return await task_service.assign_task(
            task_id, data, current_user.id, current_user.role
        )
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc
