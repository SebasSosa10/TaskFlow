from sqlalchemy import func, select

from src.modules.projects.entities.project_member import ProjectMemberModel
from src.shared.base.repository import BaseRepository


class ProjectMemberRepository(BaseRepository[ProjectMemberModel]):
    model = ProjectMemberModel

    async def get_by_project(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> list[ProjectMemberModel]:
        result = await self.session.execute(
            select(ProjectMemberModel)
            .where(ProjectMemberModel.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .order_by(ProjectMemberModel.id)
        )
        return list(result.scalars().all())

    async def count_by_project(self, project_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(ProjectMemberModel)
            .where(ProjectMemberModel.project_id == project_id)
        )
        return result.scalar_one()

    async def get_by_project_and_user(
        self, project_id: int, user_id: int
    ) -> ProjectMemberModel | None:
        result = await self.session.execute(
            select(ProjectMemberModel).where(
                ProjectMemberModel.project_id == project_id,
                ProjectMemberModel.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()
