from datetime import datetime, timezone

from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.reports.schemas.report import (
    PerformanceReportResponse,
    ProjectReportItem,
    ProjectsReportResponse,
    TaskStatusCount,
    TasksReportResponse,
    UserPerformanceReport,
    UserReportItem,
    UsersReportResponse,
)
from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.users.repositories.user_repository import UserRepository


class ReportService:
    def __init__(
        self,
        user_repository: UserRepository,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
    ) -> None:
        self.user_repository = user_repository
        self.project_repository = project_repository
        self.task_repository = task_repository

    async def get_performance_report(self) -> PerformanceReportResponse:
        users = await self.user_repository.get_all(skip=0, limit=10000)
        total_users = await self.user_repository.count()
        total_tasks = await self.task_repository.count()
        completed_tasks = await self.task_repository.count_by_status(TaskStatus.COMPLETADA)

        user_reports: list[UserPerformanceReport] = []
        for user in users:
            assigned = await self.task_repository.get_by_assignee(user.id)
            completed = [t for t in assigned if t.status == TaskStatus.COMPLETADA]
            assigned_count = len(assigned)
            completed_count = len(completed)
            completion_rate = (
                round(completed_count / assigned_count * 100, 2) if assigned_count else 0.0
            )
            user_reports.append(
                UserPerformanceReport(
                    user_id=user.id,
                    username=user.username,
                    full_name=user.full_name,
                    assigned_tasks=assigned_count,
                    completed_tasks=completed_count,
                    completion_rate=completion_rate,
                )
            )

        overall_rate = (
            round(completed_tasks / total_tasks * 100, 2) if total_tasks else 0.0
        )

        return PerformanceReportResponse(
            total_users=total_users,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            overall_completion_rate=overall_rate,
            users=user_reports,
        )

    async def get_projects_report(self) -> ProjectsReportResponse:
        projects = await self.project_repository.get_all(skip=0, limit=10000)
        total_projects = await self.project_repository.count()
        project_items: list[ProjectReportItem] = []

        for project in projects:
            total = await self.task_repository.count_by_project(project.id)
            completed = await self.task_repository.count_by_project_and_status(
                project.id, TaskStatus.COMPLETADA
            )
            in_progress = await self.task_repository.count_by_project_and_status(
                project.id, TaskStatus.EN_PROGRESO
            )
            pending = await self.task_repository.count_by_project_and_status(
                project.id, TaskStatus.PENDIENTE
            )
            blocked = await self.task_repository.count_by_project_and_status(
                project.id, TaskStatus.BLOQUEADA
            )
            completion_rate = round(completed / total * 100, 2) if total else 0.0

            project_items.append(
                ProjectReportItem(
                    project_id=project.id,
                    project_name=project.name,
                    owner_id=project.owner_id,
                    total_tasks=total,
                    completed_tasks=completed,
                    in_progress_tasks=in_progress,
                    pending_tasks=pending,
                    blocked_tasks=blocked,
                    completion_rate=completion_rate,
                )
            )

        return ProjectsReportResponse(total_projects=total_projects, projects=project_items)

    async def get_tasks_report(self) -> TasksReportResponse:
        total_tasks = await self.task_repository.count()
        by_status: list[TaskStatusCount] = []

        for status in TaskStatus:
            count = await self.task_repository.count_by_status(status)
            by_status.append(TaskStatusCount(status=status, count=count))

        return TasksReportResponse(
            total_tasks=total_tasks,
            by_status=by_status,
            generated_at=datetime.now(timezone.utc),
        )

    async def get_users_report(self) -> UsersReportResponse:
        users = await self.user_repository.get_all(skip=0, limit=10000)
        total_users = await self.user_repository.count()
        user_items: list[UserReportItem] = []

        for user in users:
            owned = await self.project_repository.get_by_owner(user.id)
            assigned = await self.task_repository.get_by_assignee(user.id, skip=0, limit=10000)
            user_items.append(UserReportItem(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                role=user.role,
                is_active=user.is_active,
                owned_projects=len(owned),
                assigned_tasks=len(assigned),
            ))

        return UsersReportResponse(total_users=total_users, users=user_items)
