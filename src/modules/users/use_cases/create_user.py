from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserCreate, UserResponse
from src.shared.exceptions.domain import AlreadyExistsError, ForbiddenError
from src.shared.security.password import hash_password
from src.shared.utils.mappers import user_to_response


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(
        self, data: UserCreate, actor_id: int, actor_role: UserRole
    ) -> UserResponse:
        if actor_role != UserRole.ADMINISTRADOR:
            raise ForbiddenError("Se requiere rol de administrador")

        if await self.user_repository.get_by_email(data.email):
            raise AlreadyExistsError("El email ya está registrado")

        if await self.user_repository.get_by_username(data.username):
            raise AlreadyExistsError("El nombre de usuario ya está en uso")

        user = await self.user_repository.create(
            {
                "email": data.email,
                "username": data.username,
                "hashed_password": hash_password(data.password),
                "full_name": data.full_name,
                "role": data.role,
                "is_active": data.is_active,
            }
        )

        await self.record_history.execute(
            actor_id, "create", "user", user.id, f"Usuario creado: {user.username}"
        )
        return user_to_response(user)
