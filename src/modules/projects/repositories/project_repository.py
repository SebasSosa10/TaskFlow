from sqlalchemy import select

from src.modules.projects.entities.project import ProjectModel
from src.shared.base.repository import BaseRepository


class ProjectRepository(BaseRepository[ProjectModel]):
    model = ProjectModel

    async def get_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[ProjectModel]:
        result = await self.session.execute(
            select(ProjectModel)
            .where(ProjectModel.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(ProjectModel.id)
        )
        return list(result.scalars().all())
