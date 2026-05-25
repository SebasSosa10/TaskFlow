from src.modules.notifications.schemas.notification import NotificationCreate, NotificationResponse
from src.modules.notifications.use_cases.create_notification import CreateNotificationUseCase
from src.modules.notifications.use_cases.get_notifications import GetNotificationsUseCase
from src.modules.users.entities.user import UserRole


class NotificationService:
    def __init__(
        self,
        get_notifications: GetNotificationsUseCase,
        create_notification: CreateNotificationUseCase,
    ) -> None:
        self._get_notifications = get_notifications
        self._create_notification = create_notification

    async def get_notifications(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[NotificationResponse], int]:
        return await self._get_notifications.execute(user_id, skip=skip, limit=limit)

    async def create_notification(
        self, data: NotificationCreate, actor_id: int, actor_role: UserRole
    ) -> NotificationResponse:
        return await self._create_notification.execute(data, actor_id, actor_role)
