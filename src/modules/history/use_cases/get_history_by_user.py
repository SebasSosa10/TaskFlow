from src.modules.history.repositories.history_repository import HistoryRepository
from src.modules.history.schemas.history import HistoryResponse
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import history_to_response


class GetHistoryByUserUseCase:
    def __init__(
        self,
        history_repository: HistoryRepository,
        user_repository: UserRepository,
    ) -> None:
        self.history_repository = history_repository
        self.user_repository = user_repository

    async def execute(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[HistoryResponse], int]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {user_id} no encontrado")

        entries = await self.history_repository.get_by_user(
            user_id, skip=skip, limit=limit
        )
        total = await self.history_repository.count_by_user(user_id)
        return [history_to_response(e) for e in entries], total
