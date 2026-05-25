from src.modules.kanban.schemas.kanban import KanbanBoardResponse, KanbanColumn
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.tasks.entities.task import TaskStatus
from src.modules.tasks.repositories.task_repository import TaskRepository
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import task_to_response


class GetKanbanBoardUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
    ) -> None:
        self.project_repository = project_repository
        self.task_repository = task_repository

    async def execute(self, project_id: int) -> KanbanBoardResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {project_id} no encontrado")

        columns: list[KanbanColumn] = []
        for status in TaskStatus:
            tasks = await self.task_repository.get_by_project_and_status(
                project_id, status
            )
            columns.append(
                KanbanColumn(
                    status=status,
                    tasks=[task_to_response(t) for t in tasks],
                )
            )

        return KanbanBoardResponse(
            project_id=project.id,
            project_name=project.name,
            columns=columns,
        )
