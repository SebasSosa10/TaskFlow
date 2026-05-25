from src.modules.projects.repositories.project_member_repository import (
    ProjectMemberRepository,
)
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project_member import ProjectMemberResponse
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import AlreadyExistsError, NotFoundError
from src.shared.utils.mappers import project_member_to_response


class GetProjectMembersUseCase:
    def __init__(
        self,
        project_member_repository: ProjectMemberRepository,
        project_repository: ProjectRepository,
    ) -> None:
        self.project_member_repository = project_member_repository
        self.project_repository = project_repository

    async def execute(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[ProjectMemberResponse], int]:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {project_id} no encontrado")

        members = await self.project_member_repository.get_by_project(
            project_id, skip=skip, limit=limit
        )
        total = await self.project_member_repository.count_by_project(project_id)
        return [project_member_to_response(m) for m in members], total
