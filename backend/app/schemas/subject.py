"""Subject schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectOut(SubjectBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
