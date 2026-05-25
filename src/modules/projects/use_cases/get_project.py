from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project import ProjectResponse
from src.shared.exceptions.domain import NotFoundError
from src.shared.utils.mappers import project_to_response


class GetProjectUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository = project_repository

    async def execute(self, project_id: int) -> ProjectResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Recurso con id {project_id} no encontrado")
        return project_to_response(project)
