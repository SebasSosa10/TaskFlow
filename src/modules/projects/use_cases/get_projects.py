from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project import ProjectResponse
from src.shared.utils.mappers import project_to_response


class GetProjectsUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository = project_repository

    async def execute(self, skip: int = 0, limit: int = 100) -> tuple[list[ProjectResponse], int]:
        projects = await self.project_repository.get_all(skip=skip, limit=limit)
        total = await self.project_repository.count()
        return [project_to_response(p) for p in projects], total
