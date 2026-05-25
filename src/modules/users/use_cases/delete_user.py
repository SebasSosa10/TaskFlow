from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import ForbiddenError, NotFoundError


class DeleteUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(self, user_id: int, actor_id: int, actor_role: UserRole) -> None:
        if actor_role != UserRole.ADMINISTRADOR:
            raise ForbiddenError("Se requiere rol de administrador")

        if actor_id == user_id:
            raise ForbiddenError("No puedes eliminar tu propio usuario")

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"Recurso con id {user_id} no encontrado")

        await self.user_repository.delete(user_id)
        await self.record_history.execute(
            actor_id, "delete", "user", user_id, f"Usuario eliminado: {user.username}"
        )
