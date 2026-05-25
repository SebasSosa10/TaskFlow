from datetime import datetime

from src.shared.base.schemas import BaseSchema


class HistoryResponse(BaseSchema):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    details: str | None
    created_at: datetime
