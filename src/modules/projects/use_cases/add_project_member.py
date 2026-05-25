from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_member_repository import (
    ProjectMemberRepository,
)
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project_member import (
    ProjectMemberCreate,
    ProjectMemberResponse,
)
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    ForbiddenError,
    NotFoundError,
)
from src.shared.utils.mappers import project_member_to_response


class AddProjectMemberUseCase:
    def __init__(
        self,
        project_member_repository: ProjectMemberRepository,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.project_member_repository = project_member_repository
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self,
        project_id: int,
        data: ProjectMemberCreate,
        actor_id: int,
        actor_role: UserRole,
    ) -> ProjectMemberResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Proyecto con id {project_id} no encontrado")

        user = await self.user_repository.get_by_id(data.user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {data.user_id} no encontrado")

        self._ensure_can_manage(actor_role, actor_id, project.owner_id)

        existing = await self.project_member_repository.get_by_project_and_user(
            project_id, data.user_id
        )
        if existing:
            raise AlreadyExistsError("El usuario ya es miembro del proyecto")

        member = await self.project_member_repository.create(
            {"project_id": project_id, "user_id": data.user_id}
        )
        await self.record_history.execute(
            actor_id,
            "add_member",
            "project",
            project_id,
            f"Miembro agregado: {user.username}",
        )
        return project_member_to_response(member)

    @staticmethod
    def _ensure_can_manage(role: UserRole, actor_id: int, owner_id: int) -> None:
        if role == UserRole.ADMINISTRADOR:
            return
        if role == UserRole.LIDER_PROYECTO and actor_id == owner_id:
            return
        raise ForbiddenError(
            "No tienes permisos para gestionar miembros de este proyecto"
        )
