from src.modules.notifications.repositories.notification_repository import NotificationRepository
from src.modules.notifications.schemas.notification import NotificationResponse
from src.shared.utils.mappers import notification_to_response


class GetNotificationsUseCase:
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self.notification_repository = notification_repository

    async def execute(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[NotificationResponse], int]:
        notifications = await self.notification_repository.get_by_user(
            user_id, skip=skip, limit=limit
        )
        total = await self.notification_repository.count_by_user(user_id)
        return [notification_to_response(n) for n in notifications], total
