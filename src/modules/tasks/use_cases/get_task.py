from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class GetTaskUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def execute(self, task_id: int) -> TaskResponse:
        task = await self.task_repository.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Recurso con id {task_id} no encontrado")
        return task_to_response(task)
