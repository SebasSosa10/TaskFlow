from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project import ProjectCreate, ProjectResponse
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from src.shared.utils.mappers import project_to_response


class CreateProjectUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self, data: ProjectCreate, actor_id: int, actor_role: UserRole
    ) -> ProjectResponse:
        owner = await self.user_repository.get_by_id(data.owner_id)
        if not owner:
            raise NotFoundError(f"Propietario con id {data.owner_id} no encontrado")

        self._ensure_can_manage(actor_role, actor_id, data.owner_id)

        project = await self.project_repository.create(data.model_dump())
        await self.record_history.execute(
            actor_id, "create", "project", project.id, f"Proyecto creado: {project.name}"
        )
        return project_to_response(project)

    @staticmethod
    def _ensure_can_manage(role: UserRole, actor_id: int, owner_id: int) -> None:
        if role == UserRole.ADMINISTRADOR:
            return
        if role == UserRole.LIDER_PROYECTO and actor_id == owner_id:
            return
        raise ForbiddenError("No tienes permisos para gestionar este proyecto")
