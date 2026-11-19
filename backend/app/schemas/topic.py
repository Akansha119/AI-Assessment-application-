"""Topic schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    subject_id: UUID
    parent_id: Optional[UUID] = None
    name: str
    description: Optional[str] = None


class TopicCreate(TopicBase):
    pass


class TopicOut(TopicBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
