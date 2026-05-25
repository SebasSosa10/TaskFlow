from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse, TaskUpdate
from src.modules.tasks.use_cases.task_permissions import (
    ensure_can_manage_project,
    validate_status_transition,
)
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class UpdateTaskUseCase:
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
        self, task_id: int, data: TaskUpdate, actor_id: int, actor_role: UserRole
    ) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        project = await self.project_repository.get_by_id(task.project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {task.project_id} no encontrado")

        ensure_can_manage_project(actor_role, actor_id, project.owner_id)

        update_data = data.model_dump(exclude_unset=True)

        if "project_id" in update_data:
            new_project = await self.project_repository.get_by_id(
                update_data["project_id"]
            )
            if not new_project:
                raise NotFoundError(
                    f"Proyecto con id {update_data['project_id']} no encontrado"
                )

        if "assignee_id" in update_data and update_data["assignee_id"] is not None:
            assignee = await self.user_repository.get_by_id(update_data["assignee_id"])
            if not assignee:
                raise NotFoundError(
                    f"Usuario con id {update_data['assignee_id']} no encontrado"
                )

        if "status" in update_data:
            validate_status_transition(task.status, update_data["status"])

        updated = await self.task_repository.update(task_id, update_data)
        if not updated:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")

        await self.record_history.execute(
            actor_id, "update", "task", task_id, f"Tarea actualizada: {updated.title}"
        )
        return task_to_response(updated)
