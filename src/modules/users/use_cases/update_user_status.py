from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse, UserStatusUpdate
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from src.shared.utils.mappers import user_to_response


class UpdateUserStatusUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self, user_id: int, data: UserStatusUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        if actor_role != UserRole.ADMINISTRADOR:
            raise ForbiddenError("Se requiere rol de administrador")

        user = await self.user_repository.update(user_id, {"is_active": data.is_active})
        if not user:
            raise NotFoundError(f"Recurso con id {user_id} no encontrado")

        status_label = "activado" if data.is_active else "desactivado"
        await self.record_history.execute(
            actor_id,
            "update_status",
            "user",
            user.id,
            f"Usuario {status_label}: {user.username}",
        )
        return user_to_response(user)
