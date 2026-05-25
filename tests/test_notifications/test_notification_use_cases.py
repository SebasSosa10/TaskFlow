import pytest

from src.modules.notifications.schemas.notification import NotificationCreate
from src.modules.notifications.use_cases.create_notification import (
    CreateNotificationUseCase,
)
from src.modules.notifications.use_cases.get_notifications import (
    GetNotificationsUseCase,
)
from src.modules.users.entities.user import UserRole
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from tests.conftest import make_notification, make_user


class TestGetNotificationsUseCase:
    async def test_get_notifications(self, notification_repo):
        notification_repo.get_by_user.return_value = [
            make_notification(id=1, user_id=1),
            make_notification(id=2, user_id=1),
        ]
        notification_repo.count_by_user.return_value = 2

        uc = GetNotificationsUseCase(notification_repo)
        notifications, total = await uc.execute(1)
        assert len(notifications) == 2
        assert total == 2

    async def test_get_notifications_empty(self, notification_repo):
        notification_repo.get_by_user.return_value = []
        notification_repo.count_by_user.return_value = 0

        uc = GetNotificationsUseCase(notification_repo)
        notifications, total = await uc.execute(1)
        assert notifications == []
        assert total == 0


class TestCreateNotificationUseCase:
    def _make_uc(self, notification_repo, user_repo):
        return CreateNotificationUseCase(notification_repo, user_repo)

    async def test_create_notification_as_admin(
        self, notification_repo, user_repo
    ):
        user_repo.get_by_id.return_value = make_user(id=2)
        notification_repo.create.return_value = make_notification(
            id=1, user_id=2, title="Alert", message="Something happened"
        )

        uc = self._make_uc(notification_repo, user_repo)
        result = await uc.execute(
            NotificationCreate(user_id=2, title="Alert", message="Something happened"),
            actor_id=1,
            actor_role=UserRole.ADMINISTRADOR,
        )
        assert result.id == 1
        assert result.user_id == 2

    async def test_create_notification_as_leader(
        self, notification_repo, user_repo
    ):
        user_repo.get_by_id.return_value = make_user(id=3)
        notification_repo.create.return_value = make_notification(id=2, user_id=3)

        uc = self._make_uc(notification_repo, user_repo)
        result = await uc.execute(
            NotificationCreate(user_id=3, title="Info", message="Task assigned"),
            actor_id=1,
            actor_role=UserRole.LIDER_PROYECTO,
        )
        assert result.id == 2

    async def test_create_notification_user_forbidden(
        self, notification_repo, user_repo
    ):
        uc = self._make_uc(notification_repo, user_repo)

        with pytest.raises(ForbiddenError, match="permisos"):
            await uc.execute(
                NotificationCreate(user_id=2, title="X", message="Y"),
                actor_id=1,
                actor_role=UserRole.USUARIO,
            )

    async def test_create_notification_target_user_not_found(
        self, notification_repo, user_repo
    ):
        user_repo.get_by_id.return_value = None
        uc = self._make_uc(notification_repo, user_repo)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(
                NotificationCreate(user_id=999, title="X", message="Y"),
                actor_id=1,
                actor_role=UserRole.ADMINISTRADOR,
            )
