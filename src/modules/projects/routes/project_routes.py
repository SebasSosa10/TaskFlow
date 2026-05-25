from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.projects.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from src.modules.projects.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse,
)
from src.modules.projects.services.project_service import ProjectService
from src.modules.tasks.schemas.task import TaskResponse
from src.modules.tasks.services.task_service import TaskService
from src.modules.users.schemas.user import UserResponse
from src.shared.base.schemas import ErrorResponse, MessageResponse, PaginatedResponse
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    DomainException,
    ForbiddenError,
)
from src.shared.middleware.dependencies import (
    get_current_active_user,
    get_project_service,
    get_task_service,
)

router = APIRouter(prefix="/projects", tags=["Proyectos"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Crear proyecto",
)
async def create_project(
    data: ProjectCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    try:
        return await project_service.create_project(
            data, current_user.id, current_user.role
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
    "",
    response_model=PaginatedResponse[ProjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar proyectos",
)
async def list_projects(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[ProjectResponse]:
    projects, total = await project_service.get_projects(skip=skip, limit=limit)
    return PaginatedResponse(items=projects, total=total, skip=skip, limit=limit)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Obtener proyecto por ID",
)
async def get_project(
    project_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    try:
        return await project_service.get_project(project_id)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    summary="Actualizar proyecto",
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    try:
        return await project_service.update_project(
            project_id, data, current_user.id, current_user.role
        )
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "no encontrado" in exc.message.lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=exc.message) from exc


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    summary="Eliminar proyecto",
)
async def delete_project(
    project_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> MessageResponse:
    try:
        await project_service.delete_project(
            project_id, current_user.id, current_user.role
        )
        return MessageResponse(message="Proyecto eliminado correctamente")
    except ForbiddenError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=exc.message
        ) from exc
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.get(
    "/{project_id}/members",
    response_model=PaginatedResponse[ProjectMemberResponse],
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Listar miembros de un proyecto",
)
async def list_project_members(
    project_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[ProjectMemberResponse]:
    try:
        members, total = await project_service.get_project_members(
            project_id, skip=skip, limit=limit
        )
        return PaginatedResponse(items=members, total=total, skip=skip, limit=limit)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc


@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    summary="Agregar miembro a un proyecto",
)
async def add_project_member(
    project_id: int,
    data: ProjectMemberCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectMemberResponse:
    try:
        return await project_service.add_project_member(
            project_id, data, current_user.id, current_user.role
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


@router.get(
    "/{project_id}/tasks",
    response_model=PaginatedResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}},
    summary="Listar tareas de un proyecto",
)
async def list_project_tasks(
    project_id: int,
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> PaginatedResponse[TaskResponse]:
    try:
        tasks, total = await task_service.get_tasks_by_project(
            project_id, skip=skip, limit=limit
        )
        return PaginatedResponse(items=tasks, total=total, skip=skip, limit=limit)
    except DomainException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.message
        ) from exc
