from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskCreate, TaskResponse
from src.modules.tasks.use_cases.task_permissions import ensure_can_manage_project
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class CreateTaskUseCase:
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
        self, data: TaskCreate, actor_id: int, actor_role: UserRole
    ) -> TaskResponse:
        project = await self.project_repository.get_by_id(data.project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {data.project_id} no encontrado")

        ensure_can_manage_project(actor_role, actor_id, project.owner_id)

        if data.assignee_id:
            assignee = await self.user_repository.get_by_id(data.assignee_id)
            if not assignee:
                raise NotFoundError(f"Usuario con id {data.assignee_id} no encontrado")

        task = await self.task_repository.create(
            {**data.model_dump(), "created_by_id": actor_id}
        )

        await self.record_history.execute(
            actor_id, "create", "task", task.id, f"Tarea creada: {task.title}"
        )
        return task_to_response(task)
