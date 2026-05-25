from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.projects.schemas.project import ProjectResponse, ProjectUpdate
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from src.shared.utils.mappers import project_to_response


class UpdateProjectUseCase:
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
        self,
        project_id: int,
        data: ProjectUpdate,
        actor_id: int,
        actor_role: UserRole,
    ) -> ProjectResponse:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Recurso con id {project_id} no encontrado")

        update_data = data.model_dump(exclude_unset=True)

        if "owner_id" in update_data:
            owner = await self.user_repository.get_by_id(update_data["owner_id"])
            if not owner:
                raise NotFoundError(f"Propietario con id {update_data['owner_id']} no encontrado")

        owner_id = update_data.get("owner_id", project.owner_id)
        self._ensure_can_manage(actor_role, actor_id, owner_id)

        updated = await self.project_repository.update(project_id, update_data)
        if not updated:
            raise NotFoundError(f"Recurso con id {project_id} no encontrado")

        await self.record_history.execute(
            actor_id, "update", "project", project_id, f"Proyecto actualizado: {updated.name}"
        )
        return project_to_response(updated)

    @staticmethod
    def _ensure_can_manage(role: UserRole, actor_id: int, owner_id: int) -> None:
        if role == UserRole.ADMINISTRADOR:
            return
        if role == UserRole.LIDER_PROYECTO and actor_id == owner_id:
            return
        raise ForbiddenError("No tienes permisos para gestionar este proyecto")
