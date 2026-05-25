from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseSchema):
    message: str


class PaginatedResponse(BaseSchema, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int


class ErrorResponse(BaseSchema):
    detail: str
    error_code: str | None = None


class TimestampMixin(BaseSchema):
    created_at: datetime | None = None
    updated_at: datetime | None = None
