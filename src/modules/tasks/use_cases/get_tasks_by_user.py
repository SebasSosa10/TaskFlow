from src.modules.tasks.repositories.task_repository import TaskRepository
from src.modules.tasks.schemas.task import TaskResponse
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class GetTasksByUserUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        user_repository: UserRepository,
    ) -> None:
        self.task_repository = task_repository
        self.user_repository = user_repository

    async def execute(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[TaskResponse], int]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")

        tasks = await self.task_repository.get_by_assignee(user_id, skip=skip, limit=limit)
        total = await self.task_repository.count_by_assignee(user_id)
        return [task_to_response(t) for t in tasks], total
