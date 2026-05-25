from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskAssignUpdate, TaskResponse
from src.modules.tasks.use_cases.task_permissions import ensure_can_manage_project
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class AssignTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self,
        task_id: int,
        data: TaskAssignUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        project = await self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {task.project_id} no encontrado")

        ensure_can_manage_project(actor_role, actor_id, project.owner_id)

        assignee = await self.user_repository.get_by_id(data.assignee_id)
        if not assignee:
            raise NotFoundError(f"Usuario con id {data.assignee_id} no encontrado")

        updated = await self.task_repository.update(
            task_id, {"assignee_id": data.assignee_id}
        )
        if not updated:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        await self.record_history.execute(
            actor_id,
            "assign",
            "task",
            task_id,
            f"Tarea asignada al usuario {data.assignee_id}",
        )
        return task_to_response(updated)
