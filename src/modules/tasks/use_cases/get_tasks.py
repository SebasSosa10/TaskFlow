from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse
from src.shared.utils.mappers import task_to_response


class GetTasksUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> tuple[list[TaskResponse], int]:
        tasks = await self.task_repository.get_all(skip=skip, limit=limit)
        total = await self.task_repository.count()
        return [task_to_response(t) for t in tasks], total
