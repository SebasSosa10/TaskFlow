from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.modules.reports.schemas.report import (
    PerformanceReportResponse,
    ProjectsReportResponse,
    TasksReportResponse,
    UsersReportResponse,
)
from src.modules.reports.services.report_service import ReportService
from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import UserResponse
from src.shared.middleware.dependencies import (
    get_current_active_user,
    get_report_service,
    require_roles,
)

router = APIRouter(prefix="/reports", tags=["Reportes"])


@router.get(
    "/performance",
    response_model=PerformanceReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Reporte de desempeño por usuario",
)
async def get_performance_report(
    _: Annotated[
        UserResponse,
        Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.LIDER_PROYECTO)),
    ],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> PerformanceReportResponse:
    return await report_service.get_performance_report()


@router.get(
    "/projects",
    response_model=ProjectsReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Reporte de proyectos",
)
async def get_projects_report(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> ProjectsReportResponse:
    return await report_service.get_projects_report()


@router.get(
    "/tasks",
    response_model=TasksReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Reporte de tareas por estado",
)
async def get_tasks_report(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> TasksReportResponse:
    return await report_service.get_tasks_report()


@router.get(
    "/users",
    response_model=UsersReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Reporte de usuarios",
)
async def get_users_report(
    _: Annotated[
        UserResponse,
        Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.LIDER_PROYECTO)),
    ],
    report_service: Annotated[ReportService, Depends(get_report_service)],
) -> UsersReportResponse:
    return await report_service.get_users_report()
