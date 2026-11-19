"""Exam-subject mapping schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ExamSubjectBase(BaseModel):
    exam_id: UUID
    subject_id: UUID
    weightage: Optional[float] = None


class ExamSubjectCreate(ExamSubjectBase):
    pass


class ExamSubjectOut(ExamSubjectBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
