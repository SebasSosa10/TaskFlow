from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class GetTasksByProjectUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self.task_repository = task_repository
        self.project_repository = project_repository

    async def execute(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {project_id} no encontrado")

        tasks = await self.task_repository.get_by_project(project_id, skip=skip, limit=limit)
        total = await self.task_repository.count_by_project(project_id)
        return [task_to_response(t) for t in tasks], total
