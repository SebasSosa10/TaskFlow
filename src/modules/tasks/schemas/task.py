from datetime import datetime

from pydantic import Field

from src.modules.tasks.entities.task import TaskStatus
from src.shared.base.schemas import BaseSchema, TimestampMixin


class TaskCreate(BaseSchema):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDIENTE
    priority: int = Field(default=1, ge=1, le=5)
    project_id: int
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskUpdate(BaseSchema):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    project_id: int | None = None
    assignee_id: int | None = None
    due_date: datetime | None = None


class TaskStatusUpdate(BaseSchema):
    status: TaskStatus


class TaskAssignUpdate(BaseSchema):
    assignee_id: int


class TaskResponse(TimestampMixin):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    project_id: int
    assignee_id: int | None
    created_by_id: int
    due_date: datetime | None
