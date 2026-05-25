from unittest.mock import patch

import pytest


from src.modules.users.entities.user import UserRole
from src.modules.users.schemas.user import (
    UserCreate,
    UserRoleUpdate,
    UserStatusUpdate,
    UserUpdate,
)
from src.modules.users.use_cases.create_user import CreateUserUseCase
from src.modules.users.use_cases.delete_user import DeleteUserUseCase
from src.modules.users.use_cases.get_user import GetUserUseCase
from src.modules.users.use_cases.get_users import GetUsersUseCase
from src.modules.users.use_cases.update_user import UpdateUserUseCase
from src.modules.users.use_cases.update_user_role import UpdateUserRoleUseCase
from src.modules.users.use_cases.update_user_status import UpdateUserStatusUseCase
from src.shared.exceptions.domain import (
    AlreadyExistsError,
    ForbiddenError,
    NotFoundError,
)
from tests.conftest import make_user


# ---------------------------------------------------------------------------
# CreateUserUseCase
# ---------------------------------------------------------------------------
class TestCreateUserUseCase:
    def _make_uc(self, user_repo, record_history):
        return CreateUserUseCase(user_repo, record_history)

    @patch("src.modules.users.use_cases.create_user.hash_password", return_value="hashed_pw")
    async def test_create_user_as_admin(self, mock_hash, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = None
        created = make_user(id=5, email="new@test.com", username="newuser")
        user_repo.create.return_value = created

        uc = self._make_uc(user_repo, record_history)
        result = await uc.execute(
            UserCreate(
                email="new@test.com",
                username="newuser",
                password="password123",
                full_name="New User",
            ),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )

        assert result.id == 5
        record_history.execute.assert_awaited_once()

    async def test_create_user_non_admin_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError, match="rol de administrador"):
            await uc.execute(
                UserCreate(
                    email="new@test.com",
                    username="newuser",
                    password="password123",
                    full_name="New",
                ),
                actor_id=1,
                actor_role=UserRole.USUARIO,
            )

    async def test_create_user_email_exists(self, user_repo, record_history):
        user_repo.get_by_email.return_value = make_user()
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(AlreadyExistsError, match="email"):
            await uc.execute(
                UserCreate(
                    email="dup@test.com",
                    username="newuser",
                    password="password123",
                    full_name="New",
                ),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_create_user_username_exists(self, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = make_user()
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(AlreadyExistsError, match="nombre de usuario"):
            await uc.execute(
                UserCreate(
                    email="new@test.com",
                    username="taken",
                    password="password123",
                    full_name="New",
                ),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# GetUserUseCase
# ---------------------------------------------------------------------------
class TestGetUserUseCase:
    async def test_get_existing_user(self, user_repo):
        user_repo.get_by_id.return_value = make_user(id=1)
        uc = GetUserUseCase(user_repo)
        result = await uc.execute(1)
        assert result.id == 1

    async def test_get_nonexistent_user(self, user_repo):
        user_repo.get_by_id.return_value = None
        uc = GetUserUseCase(user_repo)

        with pytest.raises(NotFoundError):
            await uc.execute(999)


# ---------------------------------------------------------------------------
# GetUsersUseCase
# ---------------------------------------------------------------------------
class TestGetUsersUseCase:
    async def test_get_users_list(self, user_repo):
        user_repo.get_all.return_value = [make_user(id=1), make_user(id=2)]
        user_repo.count.return_value = 2
        uc = GetUsersUseCase(user_repo)

        users, total = await uc.execute(skip=0, limit=10)
        assert len(users) == 2
        assert total == 2

    async def test_get_users_empty(self, user_repo):
        user_repo.get_all.return_value = []
        user_repo.count.return_value = 0
        uc = GetUsersUseCase(user_repo)

        users, total = await uc.execute()
        assert users == []
        assert total == 0


# ---------------------------------------------------------------------------
# UpdateUserUseCase
# ---------------------------------------------------------------------------
class TestUpdateUserUseCase:
    def _make_uc(self, user_repo, record_history):
        return UpdateUserUseCase(user_repo, record_history)

    async def test_update_user_as_admin(self, user_repo, record_history):
        updated = make_user(id=2, full_name="Updated Name")
        user_repo.update.return_value = updated
        uc = self._make_uc(user_repo, record_history)

        result = await uc.execute(
            2,
            UserUpdate(full_name="Updated Name"),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.full_name == "Updated Name"

    async def test_update_user_non_admin_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                2,
                UserUpdate(full_name="New Name"),
                actor_id=1,
                actor_role=UserRole.USUARIO,
            )

    async def test_update_user_not_found(self, user_repo, record_history):
        user_repo.update.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                UserUpdate(full_name="New Name"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_update_user_email_conflict(self, user_repo, record_history):
        existing = make_user(id=99, email="taken@test.com")
        user_repo.get_by_email.return_value = existing
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(AlreadyExistsError, match="email"):
            await uc.execute(
                2,
                UserUpdate(email="taken@test.com"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )

    async def test_update_user_username_conflict(self, user_repo, record_history):
        user_repo.get_by_email.return_value = None
        existing = make_user(id=99, username="taken")
        user_repo.get_by_username.return_value = existing
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(AlreadyExistsError, match="nombre de usuario"):
            await uc.execute(
                2,
                UserUpdate(username="taken"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# DeleteUserUseCase
# ---------------------------------------------------------------------------
class TestDeleteUserUseCase:
    def _make_uc(self, user_repo, record_history):
        return DeleteUserUseCase(user_repo, record_history)

    async def test_delete_user_as_admin(self, user_repo, record_history):
        user_repo.get_by_id.return_value = make_user(id=2, username="tobedeleted")
        uc = self._make_uc(user_repo, record_history)

        await uc.execute(user_id=2, actor_id=1, actor_role=UserRole.ADMINISTRADOR)
        user_repo.delete.assert_awaited_once_with(2)
        record_history.execute.assert_awaited_once()

    async def test_delete_user_non_admin_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(user_id=2, actor_id=1, actor_role=UserRole.USUARIO)

    async def test_delete_self_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError, match="propio usuario"):
            await uc.execute(user_id=1, actor_id=1, actor_role=UserRole.ADMINISTRADOR)

    async def test_delete_nonexistent_user(self, user_repo, record_history):
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(user_id=999, actor_id=1, actor_role=UserRole.ADMINISTRADOR)


# ---------------------------------------------------------------------------
# UpdateUserRoleUseCase
# ---------------------------------------------------------------------------
class TestUpdateUserRoleUseCase:
    def _make_uc(self, user_repo, record_history):
        return UpdateUserRoleUseCase(user_repo, record_history)

    async def test_update_role_as_admin(self, user_repo, record_history):
        updated = make_user(id=2, role=UserRole.LIDER_PROYECTO)
        user_repo.update.return_value = updated
        uc = self._make_uc(user_repo, record_history)

        result = await uc.execute(
            2,
            UserRoleUpdate(role=UserRole.LIDER_PROYECTO),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.role == UserRole.LIDER_PROYECTO

    async def test_update_role_non_admin_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                2,
                UserRoleUpdate(role=UserRole.ADMINISTRADOR),
                actor_id=1,
                actor_role=UserRole.LIDER_PROYECTO,
            )

    async def test_update_role_user_not_found(self, user_repo, record_history):
        user_repo.update.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                UserRoleUpdate(role=UserRole.USUARIO),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )


# ---------------------------------------------------------------------------
# UpdateUserStatusUseCase
# ---------------------------------------------------------------------------
class TestUpdateUserStatusUseCase:
    def _make_uc(self, user_repo, record_history):
        return UpdateUserStatusUseCase(user_repo, record_history)

    async def test_deactivate_user(self, user_repo, record_history):
        updated = make_user(id=2, is_active=False)
        user_repo.update.return_value = updated
        uc = self._make_uc(user_repo, record_history)

        result = await uc.execute(
            2,
            UserStatusUpdate(is_active=False),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.is_active is False

    async def test_activate_user(self, user_repo, record_history):
        updated = make_user(id=2, is_active=True)
        user_repo.update.return_value = updated
        uc = self._make_uc(user_repo, record_history)

        result = await uc.execute(
            2,
            UserStatusUpdate(is_active=True),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.is_active is True

    async def test_update_status_non_admin_forbidden(self, user_repo, record_history):
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(ForbiddenError):
            await uc.execute(
                2,
                UserStatusUpdate(is_active=False),
                actor_id=1,
                actor_role=UserRole.USUARIO,
            )

    async def test_update_status_user_not_found(self, user_repo, record_history):
        user_repo.update.return_value = None
        uc = self._make_uc(user_repo, record_history)

        with pytest.raises(NotFoundError):
            await uc.execute(
                999,
                UserStatusUpdate(is_active=False),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )
