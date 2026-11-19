"""Syllabus version schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SyllabusVersionBase(BaseModel):
    exam_id: UUID
    version: str
    title: str
    description: Optional[str] = None
    effective_from: Optional[str] = None
    is_active: bool = True


class SyllabusVersionCreate(SyllabusVersionBase):
    pass


class SyllabusVersionOut(SyllabusVersionBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
