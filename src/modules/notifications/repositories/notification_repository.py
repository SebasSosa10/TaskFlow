from sqlalchemy import func, select

from src.modules.notifications.entities.notification import NotificationModel
from src.shared.base.repository import BaseRepository


class NotificationRepository(BaseRepository[NotificationModel]):
    model = NotificationModel

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[NotificationModel]:
        result = await self.session.execute(
            select(NotificationModel)
            .where(NotificationModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(NotificationModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_by_user(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(NotificationModel)
            .where(NotificationModel.user_id == user_id)
        )
        return result.scalar_one()
