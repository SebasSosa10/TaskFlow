from src.modules.notifications.repositories.notification_repository import NotificationRepository
from src.modules.notifications.schemas.notification import NotificationCreate, NotificationResponse
from src.modules.users.entities.user import UserRole
from src.modules.users.repositories.user_repository import UserRepository
from src.shared.exceptions.domain import ForbiddenError, NotFoundError
from src.shared.utils.mappers import notification_to_response


class CreateNotificationUseCase:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        user_repository: UserRepository,
    ) -> None:
        self.notification_repository = notification_repository
        self.user_repository = user_repository

    async def execute(
        self, data: NotificationCreate, actor_id: int, actor_role: UserRole
    ) -> NotificationResponse:
        if actor_role not in (UserRole.ADMINISTRADOR, UserRole.LIDER_PROYECTO):
            raise ForbiddenError("No tienes permisos para crear notificaciones")

        user = await self.user_repository.get_by_id(data.user_id)
        if not user:
            raise NotFoundError(f"Usuario con id {data.user_id} no encontrado")

        notification = await self.notification_repository.create(data.model_dump())
        return notification_to_response(notification)
