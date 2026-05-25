from src.modules.history.entities.history import HistoryModel
from src.modules.history.schemas.history import HistoryResponse
from src.modules.notifications.entities.notification import NotificationModel
from src.modules.notifications.schemas.notification import NotificationResponse
from src.modules.projects.entities.project import ProjectModel
from src.modules.projects.entities.project_member import ProjectMemberModel
from src.modules.projects.schemas.project import ProjectResponse
from src.modules.projects.schemas.project_member import ProjectMemberResponse
from src.modules.tasks.entities.task import TaskModel
from src.modules.tasks.schemas.task import TaskResponse
from src.modules.users.entities.user import UserModel
from src.modules.users.schemas.user import UserResponse


def user_to_response(user: UserModel) -> UserResponse:
    return UserResponse.model_validate(user)


def project_to_response(project: ProjectModel) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


def project_member_to_response(member: ProjectMemberModel) -> ProjectMemberResponse:
    return ProjectMemberResponse.model_validate(member)


def task_to_response(task: TaskModel) -> TaskResponse:
    return TaskResponse.model_validate(task)


def history_to_response(entry: HistoryModel) -> HistoryResponse:
    return HistoryResponse.model_validate(entry)


def notification_to_response(notification: NotificationModel) -> NotificationResponse:
    return NotificationResponse.model_validate(notification)
