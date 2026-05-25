from src.modules.history.repositories.history_repository import HistoryRepository
from src.modules.history.schemas.history import HistoryResponse
from src.shared.utils.mappers import history_to_response


class GetHistoryUseCase:
    def __init__(self, history_repository: HistoryRepository) -> None:
        self.history_repository = history_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> tuple[list[HistoryResponse], int]:
        entries = await self.history_repository.get_all(skip=skip, limit=limit)
        total = await self.history_repository.count()
        return [history_to_response(e) for e in entries], total
