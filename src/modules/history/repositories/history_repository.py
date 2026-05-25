from sqlalchemy import func, select

from src.modules.history.entities.history import HistoryModel
from src.shared.base.repository import BaseRepository


class HistoryRepository(BaseRepository[HistoryModel]):
    model = HistoryModel

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[HistoryModel]:
        result = await self.session.execute(
            select(HistoryModel)
            .offset(skip)
            .limit(limit)
            .order_by(HistoryModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[HistoryModel]:
        result = await self.session.execute(
            select(HistoryModel)
            .where(HistoryModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(HistoryModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_entity(
        self, entity_type: str, entity_id: int, skip: int = 0, limit: int = 100
    ) -> list[HistoryModel]:
        result = await self.session.execute(
            select(HistoryModel)
            .where(
                HistoryModel.entity_type == entity_type,
                HistoryModel.entity_id == entity_id,
            )
            .offset(skip)
            .limit(limit)
            .order_by(HistoryModel.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_by_user(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(HistoryModel)
            .where(HistoryModel.user_id == user_id)
        )
        return result.scalar_one()
