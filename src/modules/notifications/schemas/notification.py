from datetime import datetime

from pydantic import Field

from src.shared.base.schemas import BaseSchema


class NotificationCreate(BaseSchema):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    message: str = Field(min_length=1)


class NotificationResponse(BaseSchema):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
