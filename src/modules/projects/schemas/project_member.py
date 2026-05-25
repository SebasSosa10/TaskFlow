from datetime import datetime

from pydantic import Field

from src.shared.base.schemas import BaseSchema


class ProjectMemberCreate(BaseSchema):
    user_id: int = Field(gt=0)


class ProjectMemberResponse(BaseSchema):
    id: int
    project_id: int
    user_id: int
    joined_at: datetime
