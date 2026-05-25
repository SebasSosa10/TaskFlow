from src.modules.kanban.schemas.kanban import KanbanBoardResponse
from src.modules.kanban.use_cases.get_kanban_board import GetKanbanBoardUseCase


class KanbanService:
    def __init__(self, get_kanban_board: GetKanbanBoardUseCase) -> None:
        self._get_kanban_board = get_kanban_board

    async def get_board(self, project_id: int) -> KanbanBoardResponse:
        return await self._get_kanban_board.execute(project_id)
