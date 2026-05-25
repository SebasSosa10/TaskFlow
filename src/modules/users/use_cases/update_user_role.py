from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse, UserRoleUpdate
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from src.shared.utils.mappers import user_to_response


class UpdateUserRoleUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self, user_id: int, data: UserRoleUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        if actor_role != UserRole.ADMINISTRADOR:
            raise ForbiddenError("Se requiere rol de administrador")

        user = await self.user_repository.update(user_id, {"role": data.role})
        if not user:
            raise NotFoundError(f"Recurso con id {user_id} no encontrado")

        await self.record_history.execute(
            actor_id,
            "update_role",
            "user",
            user.id,
            f"Rol actualizado a {data.role.value}: {user.username}",
        )
        return user_to_response(user)
