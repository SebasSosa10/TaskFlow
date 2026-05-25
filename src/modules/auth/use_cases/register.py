from src.modules.auth.schemas.auth import RegisterRequest
from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.schemas.user import UserResponse
from src.shared.exceptions.domain import AlreadyExistsError, ForbiddenError
from src.shared.security.password import hash_password
from src.shared.utils.mappers import user_to_response


class RegisterUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(self, data: RegisterRequest) -> UserResponse:
        if await self.user_repository.get_by_email(data.email):
            raise AlreadyExistsError("El email ya está registrado")

        if await self.user_repository.get_by_username(data.username):
            raise AlreadyExistsError("El nombre de usuario ya está en uso")

        if data.role != UserRole.USUARIO:
            raise ForbiddenError("Solo se permite registrar usuarios con rol 'usuario'")

        user = await self.user_repository.create(
            {
                "email": data.email,
                "username": data.username,
                "hashed_password": hash_password(data.password),
                "full_name": data.full_name,
                "role": data.role,
                "is_active": True,
            }
        )

        await self.record_history.execute(
            user.id, "register", "user", user.id, f"Usuario registrado: {user.username}"
        )

        return user_to_response(user)
