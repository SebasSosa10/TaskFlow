from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse
from src.shared.utils.mappers import task_to_response


class GetTasksByStatusUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def execute(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        tasks = await self.task_repository.get_by_status(status, skip=skip, limit=limit)
        total = await self.task_repository.count_by_status(status)
        return [task_to_response(t) for t in tasks], total
