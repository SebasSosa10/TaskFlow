from src.modules.projects.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from src.modules.projects.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse,
)
from src.modules.projects.use_cases.add_project_member import AddProjectMemberUseCase
from src.modules.projects.use_cases.create_project import CreateProjectUseCase
from src.modules.projects.use_cases.delete_project import DeleteProjectUseCase
from src.modules.projects.use_cases.get_project import GetProjectUseCase
from src.modules.projects.use_cases.get_project_members import GetProjectMembersUseCase
from src.modules.projects.use_cases.get_projects import GetProjectsUseCase
from src.modules.projects.use_cases.update_project import UpdateProjectUseCase
from src.modules.users.entities.user import UserRole


class ProjectService:
    def __init__(
        self,
        create_project: CreateProjectUseCase,
        get_projects: GetProjectsUseCase,
        get_project: GetProjectUseCase,
        update_project: UpdateProjectUseCase,
        delete_project: DeleteProjectUseCase,
        get_project_members: GetProjectMembersUseCase,
        add_project_member: AddProjectMemberUseCase,
    ) -> None:
        self._create_project = create_project
        self._get_projects = get_projects
        self._get_project = get_project
        self._update_project = update_project
        self._delete_project = delete_project
        self._get_project_members = get_project_members
        self._add_project_member = add_project_member

    async def create_project(
        self, data: ProjectCreate, actor_id: int, actor_role: UserRole
    ) -> ProjectResponse:
        return await self._create_project.execute(data, actor_id, actor_role)

    async def get_projects(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[ProjectResponse], int]:
        return await self._get_projects.execute(skip=skip, limit=limit)

    async def get_project(self, project_id: int) -> ProjectResponse:
        return await self._get_project.execute(project_id)

    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> ProjectResponse:
        return await self._update_project.execute(
            project_id, data, actor_id, actor_role
        )

    async def delete_project(
        self, project_id: int, actor_id: int, actor_role: UserRole
    ) -> None:
        await self._delete_project.execute(project_id, actor_id, actor_role)

    async def get_project_members(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[ProjectMemberResponse], int]:
        return await self._get_project_members.execute(
            project_id, skip=skip, limit=limit
        )

    async def add_project_member(
        self,
        project_id: int,
        data: ProjectMemberCreate,
        actor_id: int,
        actor_role: UserRole,
    ) -> ProjectMemberResponse:
        return await self._add_project_member.execute(
            project_id, data, actor_id, actor_role
        )
