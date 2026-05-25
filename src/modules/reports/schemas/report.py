from datetime import datetime

from src.modules.tasks.entities.task import TaskStatus
from src.modules.users.entities.user import UserRole
from src.shared.base.schemas import BaseSchema


class TaskStatusCount(BaseSchema):
    status: TaskStatus
    count: int


class UserPerformanceReport(BaseSchema):
    user_id: int
    username: str
    full_name: str
    assigned_tasks: int
    completed_tasks: int
    completion_rate: float


class PerformanceReportResponse(BaseSchema):
    total_users: int
    total_tasks: int
    completed_tasks: int
    overall_completion_rate: float
    users: list[UserPerformanceReport]


class ProjectReportItem(BaseSchema):
    project_id: int
    project_name: str
    owner_id: int
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    pending_tasks: int
    blocked_tasks: int
    completion_rate: float


class ProjectsReportResponse(BaseSchema):
    total_projects: int
    projects: list[ProjectReportItem]


class TasksReportResponse(BaseSchema):
    total_tasks: int
    by_status: list[TaskStatusCount]
    generated_at: datetime


class UserReportItem(BaseSchema):
    user_id: int
    username: str
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    owned_projects: int
    assigned_tasks: int


class UsersReportResponse(BaseSchema):
    total_users: int
    users: list[UserReportItem]
