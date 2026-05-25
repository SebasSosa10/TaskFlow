from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.schemas.task import TaskResponse
from src.shared.base.schemas import BaseSchema


class KanbanColumn(BaseSchema):
    status: TaskStatus
    tasks: list[TaskResponse]


class KanbanBoardResponse(BaseSchema):
    project_id: int
    project_name: str
    columns: list[KanbanColumn]
