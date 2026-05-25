from unittest.mock import patch

import pytest

from src.modules.auth.schemas.auth import RegisterRequest
from src.modules.auth.use_cases.register import RegisterUseCase
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import AlreadyExistsError, ForbiddenError
from tests.conftest import make_user


class TestRegisterUseCase:
    def _make_uc(self, user_repo, record_history):
        return RegisterUseCase(user_repo, record_history)

    @patch(
        "src.modules.auth.use_cases.register.hash_password", return_value="hashed_pw"
    )
    async def test_register_success(self, mock_hash, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = None
        created = make_user(id=10, email="new@test.com", username="newuser")
        user_repo.create.return_value = created

        uc = self._make_uc(user_repo, record_history)
        result = await uc.execute(
            RegisterRequest(
                email="new@test.com",
                username="newuser",
                password="password123",
                full_name="New User",
            )
        )

        assert result.id == 10
        assert result.email == "new@test.com"
        user_repo.create.assert_awaited_once()
        record_history.execute.assert_awaited_once()

    async def test_register_email_already_exists(self, user_repo, record_history):
        user_repo.get_by_email.return_value = make_user(email="existing@test.com")
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(AlreadyExistsError, match="email ya está registrado"):
            await uc.execute(
                RegisterRequest(
                    email="existing@test.com",
                    username="newuser",
                    password="password123",
                    full_name="Test",
                )
            )

    async def test_register_username_already_exists(self, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = make_user(username="taken")
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(
            AlreadyExistsError, match="nombre de usuario ya está en uso"
        ):
            await uc.execute(
                RegisterRequest(
                    email="new@test.com",
                    username="taken",
                    password="password123",
                    full_name="Test",
                )
            )

    async def test_register_non_user_role_forbidden(self, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError, match="Solo se permite registrar"):
            await uc.execute(
                RegisterRequest(
                    email="new@test.com",
                    username="newuser",
                    password="password123",
                    full_name="Test",
                    role=UserRole.ADMINISTRADOR,
                )
            )
