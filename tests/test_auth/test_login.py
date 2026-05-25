from unittest.mock import AsyncMock, patch

import pytest

from src.modules.auth.schemas.auth import LoginRequest
from src.modules.auth.use_cases.login import LoginUseCase
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import ForbiddenError, UnauthorizedError
from tests.conftest import make_user


class TestLoginUseCase:
    def _make_uc(self, user_repo, record_history):
        return LoginUseCase(user_repo, record_history)

    async def test_login_success(self, user_repo, record_history):
        user = make_user(id=1, username="testuser", role=UserRole.USUARIO)
        user_repo.get_by_username.return_value = user

        with patch(
            "src.modules.auth.use_cases.login.verify_password", return_value=True
        ):
            uc = self._make_uc(user_repo, record_history)
            result = await uc.execute(
                LoginRequest(username="testuser", password="password123")
            )

        assert result.access_token
        assert result.token_type == "bearer"
        record_history.execute.assert_awaited_once()

    async def test_login_wrong_password(self, user_repo, record_history):
        user = make_user(username="testuser")
        user_repo.get_by_username.return_value = user

        with patch(
            "src.modules.auth.use_cases.login.verify_password", return_value=False
        ):
            uc = self._make_uc(user_repo, record_history)
            with pytest.raises(UnauthorizedError, match="Credenciales inválidas"):
                await uc.execute(
                    LoginRequest(username="testuser", password="wrongpass")
                )

    async def test_login_user_not_found(self, user_repo, record_history):
        user_repo.get_by_username.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(UnauthorizedError, match="Credenciales inválidas"):
            await uc.execute(LoginRequest(username="noexiste", password="password123"))

    async def test_login_inactive_user(self, user_repo, record_history):
        user = make_user(username="testuser", is_active=False)
        user_repo.get_by_username.return_value = user

        with patch(
            "src.modules.auth.use_cases.login.verify_password", return_value=True
        ):
            uc = self._make_uc(user_repo, record_history)
            with pytest.raises(ForbiddenError, match="Usuario inactivo"):
                await uc.execute(
                    LoginRequest(username="testuser", password="password123")
                )
