from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.use_cases.task_permissions import ensure_can_manage_project
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import NotFoundError


class DeleteTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.record_history = record_history

    async def execute(self, task_id: int, actor_id: int, actor_role: UserRole) -> None:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        project = await self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {task.project_id} no encontrado")

        ensure_can_manage_project(actor_role, actor_id, project.owner_id)

        await self.task_repository.delete(task_id)
        await self.record_history.execute(
            actor_id, "delete", "task", task_id, f"Tarea eliminada: {task.title}"
        )
