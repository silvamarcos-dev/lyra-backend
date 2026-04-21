from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ReminderCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    remind_at: datetime
    channel: str = "in_app"


class ReminderResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    remind_at: datetime
    channel: str
    status: str
    sent: bool


class ReminderListResponse(BaseModel):
    reminders: List[ReminderResponse]
    total: int