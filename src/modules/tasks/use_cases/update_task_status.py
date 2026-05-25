from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse, TaskStatusUpdate
from src.modules.tasks.use_cases.task_permissions import (
    ensure_can_work_on_task,
    validate_status_transition,
)
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class UpdateTaskStatusUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.record_history = record_history

    async def execute(
        self,
        task_id: int,
        data: TaskStatusUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        project = await self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {task.project_id} no encontrado")

        ensure_can_work_on_task(actor_role, actor_id, project.owner_id, task)
        validate_status_transition(task.status, data.status)

        updated = await self.task_repository.update(task_id, {"status": data.status})
        if not updated:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        await self.record_history.execute(
            actor_id,
            "status_change",
            "task",
            task_id,
            f"Estado cambiado de '{task.status.value}' a '{data.status.value}'",
        )
        return task_to_response(updated)
