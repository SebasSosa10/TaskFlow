from src.modules.history.schemas.history import HistoryResponse
from src.modules.history.use_cases.get_history import GetHistoryUseCase
from src.modules.history.use_cases.get_history_by_user import GetHistoryByUserUseCase


class HistoryService:
    def __init__(
        self,
        get_history: GetHistoryUseCase,
        get_history_by_user: GetHistoryByUserUseCase,
    ) -> None:
        self._get_history = get_history
        self._get_history_by_user = get_history_by_user

    async def get_history(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[HistoryResponse], int]:
        return await self._get_history.execute(skip=skip, limit=limit)

    async def get_history_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[HistoryResponse], int]:
        return await self._get_history_by_user.execute(user_id, skip=skip, limit=limit)
