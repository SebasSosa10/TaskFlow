from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse, UserUpdate
from src.shared.exceptions.domain import AlreadyExistsError, ForbiddenError, NotFoundError
from src.shared.security.password import hash_password
from src.shared.utils.mappers import user_to_response


class UpdateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self, user_id: int, data: UserUpdate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        if actor_role != UserRole.ADMINISTRADOR:
            raise ForbiddenError("Se requiere rol de administrador")

        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = await self.user_repository.get_by_email(update_data["email"])
            if existing and existing.id != user_id:
                raise AlreadyExistsError("El email ya está registrado")

        if "username" in update_data:
            existing = await self.user_repository.get_by_username(update_data["username"])
            if existing and existing.id != user_id:
                raise AlreadyExistsError("El nombre de usuario ya está en uso")

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        user = await self.user_repository.update(user_id, update_data)
        if not user:
            raise NotFoundError(f"Recurso con id {user_id} no encontrado")

        await self.record_history.execute(
            actor_id, "update", "user", user.id, f"Usuario actualizado: {user.username}"
        )
        return user_to_response(user)
