"""Exam pattern schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ExamPatternBase(BaseModel):
    exam_id: UUID
    name: str
    total_questions: Optional[int] = None
    marks_per_correct: Optional[float] = None
    negative_marking_penalty: Optional[float] = None
    duration_minutes: Optional[int] = None
    difficulty_distribution: Optional[str] = None
    is_default: bool = False


class ExamPatternCreate(ExamPatternBase):
    pass


class ExamPatternOut(ExamPatternBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
