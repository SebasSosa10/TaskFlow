from src.modules.auth.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.modules.auth.use_cases.login import LoginUseCase
from src.modules.auth.use_cases.register import RegisterUseCase
from src.modules.users.schemas.user import UserResponse


class AuthService:
    def __init__(self, login: LoginUseCase, register: RegisterUseCase) -> None:
        self._login = login
        self._register = register

    async def login(self, credentials: LoginRequest) -> TokenResponse:
        return await self._login.execute(credentials)

    async def register(self, data: RegisterRequest) -> UserResponse:
        return await self._register.execute(data)
