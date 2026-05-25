from sqlalchemy import func, select

from src.modules.tasks.entities.task import TaskModel, TaskStatus
from src.shared.base.repository import BaseRepository


class TaskRepository(BaseRepository[TaskModel]):
    model = TaskModel

    async def get_by_project(
        self, project_id: int, skip: int = 0, limit: int = 100
    ) -> list[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .where(TaskModel.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .order_by(TaskModel.id)
        )
        return list(result.scalars().all())

    async def get_by_project_and_status(
        self, project_id: int, status: TaskStatus
    ) -> list[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .where(TaskModel.project_id == project_id, TaskModel.status == status)
            .order_by(TaskModel.priority.desc(), TaskModel.id)
        )
        return list(result.scalars().all())

    async def get_by_status(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> list[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .where(TaskModel.status == status)
            .offset(skip)
            .limit(limit)
            .order_by(TaskModel.id)
        )
        return list(result.scalars().all())

    async def get_by_assignee(
        self, assignee_id: int, skip: int = 0, limit: int = 100
    ) -> list[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .where(TaskModel.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
            .order_by(TaskModel.id)
        )
        return list(result.scalars().all())

    async def count_by_assignee(self, assignee_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.assignee_id == assignee_id)
        )
        return result.scalar_one()

    async def count_by_status(self, status: TaskStatus) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.status == status)
        )
        return result.scalar_one()

    async def count_by_project(self, project_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.project_id == project_id)
        )
        return result.scalar_one()

    async def count_by_project_and_status(
        self, project_id: int, status: TaskStatus
    ) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.project_id == project_id, TaskModel.status == status)
        )
        return result.scalar_one()
