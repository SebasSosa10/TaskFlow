from src.modules.history.repositories.history_repository import HistoryRepository


class RecordHistoryUseCase:
    def __init__(self, history_repository: HistoryRepository) -> None:
        self.history_repository = history_repository

    async def execute(
        self,
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        details: str,
    ) -> None:
        await self.history_repository.create(
            {
                "user_id": user_id,
                "action": action,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "details": details,
            }
        )
