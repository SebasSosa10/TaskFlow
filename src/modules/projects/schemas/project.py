from pydantic import Field

from src.modules.projects.entities.project import ProjectStatus
from src.shared.base.schemas import BaseSchema, TimestampMixin


class ProjectCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    owner_id: int
    status: ProjectStatus = ProjectStatus.ACTIVO


class ProjectUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    owner_id: int | None = None
    status: ProjectStatus | None = None


class ProjectResponse(TimestampMixin):
    id: int
    name: str
    description: str | None
    owner_id: int
    status: ProjectStatus
