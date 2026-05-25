from src.modules.auth.schemas.auth import LoginRequest, TokenResponse
from src.modules.auth.security.token import create_access_token
from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import ForbiddenError, UnauthorizedError
from src.shared.security.password import verify_password


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        record_history: RecordHistoryUseCase,
    ) -> None:
        self.user_repository = user_repository
        self.record_history = record_history

    async def execute(self, credentials: LoginRequest) -> TokenResponse:
        user = await self.user_repository.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedError("Credenciales inválidas")

        if not user.is_active:
            raise ForbiddenError("Usuario inactivo")

        token = create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.role.value}
        )

        await self.record_history.execute(
            user.id, "login", "user", user.id, "Inicio de sesión exitoso"
        )

        return TokenResponse(access_token=token)
