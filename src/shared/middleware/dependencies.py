from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.security.token import decode_access_token
from src.modules.auth.services.auth_service import AuthService
from src.modules.auth.use_cases.login import LoginUseCase
from src.modules.auth.use_cases.register import RegisterUseCase
from src.modules.history.repositories.history_repository import HistoryRepository
from src.modules.history.services.history_service import HistoryService
from src.modules.history.use_cases.get_history import GetHistoryUseCase
from src.modules.history.use_cases.get_history_by_user import GetHistoryByUserUseCase
from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.kanban.services.kanban_service import KanbanService
from src.modules.kanban.use_cases.get_kanban_board import GetKanbanBoardUseCase
from src.modules.notifications.repositories.notification_repository import (
    NotificationRepository,
)
from src.modules.notifications.services.notification_service import NotificationService
from src.modules.notifications.use_cases.create_notification import (
    CreateNotificationUseCase,
)
from src.modules.notifications.use_cases.get_notifications import (
    GetNotificationsUseCase,
)
from src.modules.projects.repositories.project_member_repository import (
    ProjectMemberRepository,
)
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.services.project_service import ProjectService
from src.modules.projects.use_cases.add_project_member import AddProjectMemberUseCase
from src.modules.projects.use_cases.create_project import CreateProjectUseCase
from src.modules.projects.use_cases.delete_project import DeleteProjectUseCase
from src.modules.projects.use_cases.get_project import GetProjectUseCase
from src.modules.projects.use_cases.get_project_members import GetProjectMembersUseCase
from src.modules.projects.use_cases.get_projects import GetProjectsUseCase
from src.modules.projects.use_cases.update_project import UpdateProjectUseCase
from src.modules.reports.services.report_service import ReportService
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.services.task_service import TaskService
from src.modules.tasks.use_cases.assign_task import AssignTaskUseCase
from src.modules.tasks.use_cases.create_task import CreateTaskUseCase
from src.modules.tasks.use_cases.delete_task import DeleteTaskUseCase
from src.modules.tasks.use_cases.get_task import GetTaskUseCase
from src.modules.tasks.use_cases.get_tasks import GetTasksUseCase
from src.modules.tasks.use_cases.get_tasks_by_project import GetTasksByProjectUseCase
from src.modules.tasks.use_cases.get_tasks_by_status import GetTasksByStatusUseCase
from src.modules.tasks.use_cases.get_tasks_by_user import GetTasksByUserUseCase
from src.modules.tasks.use_cases.update_task import UpdateTaskUseCase
from src.modules.tasks.use_cases.update_task_status import UpdateTaskStatusUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse
from src.modules.users.services.user_service import UserService
from src.modules.users.use_cases.create_user import CreateUserUseCase
from src.modules.users.use_cases.delete_user import DeleteUserUseCase
from src.modules.users.use_cases.get_user import GetUserUseCase
from src.modules.users.use_cases.get_users import GetUsersUseCase
from src.modules.users.use_cases.update_user import UpdateUserUseCase
from src.modules.users.use_cases.update_user_role import UpdateUserRoleUseCase
from src.modules.users.use_cases.update_user_status import UpdateUserStatusUseCase
from src.shared.database.session import get_db_session
from src.shared.exceptions.domain import UnauthorizedError
from src.shared.utils.mappers import user_to_response

security = HTTPBearer(auto_error=False)


async def get_db(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AsyncSession:
    return session


def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_project_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_member_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectMemberRepository:
    return ProjectMemberRepository(db)


def get_task_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> TaskRepository:
    return TaskRepository(db)


def get_history_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HistoryRepository:
    return HistoryRepository(db)


def get_notification_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NotificationRepository:
    return NotificationRepository(db)


def get_record_history(
    history_repo: Annotated[HistoryRepository, Depends(get_history_repository)],
) -> RecordHistoryUseCase:
    return RecordHistoryUseCase(history_repo)


def get_auth_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    record_history: Annotated[RecordHistoryUseCase, Depends(get_record_history)],
) -> AuthService:
    return AuthService(
        login=LoginUseCase(user_repo, record_history),
        register=RegisterUseCase(user_repo, record_history),
    )


def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    record_history: Annotated[RecordHistoryUseCase, Depends(get_record_history)],
) -> UserService:
    return UserService(
        create_user=CreateUserUseCase(user_repo, record_history),
        get_users=GetUsersUseCase(user_repo),
        get_user=GetUserUseCase(user_repo),
        update_user=UpdateUserUseCase(user_repo, record_history),
        delete_user=DeleteUserUseCase(user_repo, record_history),
        update_user_role=UpdateUserRoleUseCase(user_repo, record_history),
        update_user_status=UpdateUserStatusUseCase(user_repo, record_history),
    )


def get_project_service(
    project_repo: Annotated[ProjectRepository, Depends(get_project_repository)],
    project_member_repo: Annotated[
        ProjectMemberRepository, Depends(get_project_member_repository)
    ],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    record_history: Annotated[RecordHistoryUseCase, Depends(get_record_history)],
) -> ProjectService:
    return ProjectService(
        create_project=CreateProjectUseCase(project_repo, user_repo, record_history),
        get_projects=GetProjectsUseCase(project_repo),
        get_project=GetProjectUseCase(project_repo),
        update_project=UpdateProjectUseCase(project_repo, user_repo, record_history),
        delete_project=DeleteProjectUseCase(project_repo, record_history),
        get_project_members=GetProjectMembersUseCase(project_member_repo, project_repo),
        add_project_member=AddProjectMemberUseCase(
            project_member_repo, project_repo, user_repo, record_history
        ),
    )


def get_task_service(
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
    project_repo: Annotated[ProjectRepository, Depends(get_project_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    record_history: Annotated[RecordHistoryUseCase, Depends(get_record_history)],
) -> TaskService:
    return TaskService(
        create_task=CreateTaskUseCase(
            task_repo, project_repo, user_repo, record_history
        ),
        get_tasks=GetTasksUseCase(task_repo),
        get_task=GetTaskUseCase(task_repo),
        get_tasks_by_project=GetTasksByProjectUseCase(task_repo, project_repo),
        get_tasks_by_user=GetTasksByUserUseCase(task_repo, user_repo),
        get_tasks_by_status=GetTasksByStatusUseCase(task_repo),
        update_task=UpdateTaskUseCase(
            task_repo, project_repo, user_repo, record_history
        ),
        delete_task=DeleteTaskUseCase(task_repo, project_repo, record_history),
        update_status=UpdateTaskStatusUseCase(task_repo, project_repo, record_history),
        assign_task=AssignTaskUseCase(
            task_repo, project_repo, user_repo, record_history
        ),
    )


def get_report_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    project_repo: Annotated[ProjectRepository, Depends(get_project_repository)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
) -> ReportService:
    return ReportService(user_repo, project_repo, task_repo)


def get_history_service(
    history_repo: Annotated[HistoryRepository, Depends(get_history_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> HistoryService:
    return HistoryService(
        get_history=GetHistoryUseCase(history_repo),
        get_history_by_user=GetHistoryByUserUseCase(history_repo, user_repo),
    )


def get_kanban_service(
    project_repo: Annotated[ProjectRepository, Depends(get_project_repository)],
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)],
) -> KanbanService:
    return KanbanService(GetKanbanBoardUseCase(project_repo, task_repo))


def get_notification_service(
    notification_repo: Annotated[
        NotificationRepository, Depends(get_notification_repository)
    ],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> NotificationService:
    return NotificationService(
        get_notifications=GetNotificationsUseCase(notification_repo),
        create_notification=CreateNotificationUseCase(notification_repo, user_repo),
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("user_id")
        if user_id is None:
            raise UnauthorizedError("Token inválido")
    except (ValueError, UnauthorizedError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = await user_repo.get_by_id(int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_to_response(user)


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    return current_user


def require_roles(*roles: UserRole):
    async def role_checker(
        current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    ) -> UserResponse:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes",
            )
        return current_user

    return role_checker
