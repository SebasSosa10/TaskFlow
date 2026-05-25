from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.projects.repositories.project_repository import ProjectRepository
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import ForbiddenError, NotFoundError


class DeleteProjectUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.project_repository = project_repository
        self.record_history = record_history

    async def execute(self, project_id: int, actor_id: int, actor_role: UserRole) -> None:
        project = await self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Recurso con id {project_id} no encontrado")

        if actor_role == UserRole.ADMINISTRADOR:
            pass
        elif actor_role == UserRole.LIDER_PROYECTO and actor_id == project.owner_id:
            pass
        else:
            raise ForbiddenError("No tienes permisos para gestionar este proyecto")

        await self.project_repository.delete(project_id)
        await self.record_history.execute(
            actor_id, "delete", "project", project_id, f"Proyecto eliminado: {project.name}"
        )
