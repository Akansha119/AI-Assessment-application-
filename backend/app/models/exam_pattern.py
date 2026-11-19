"""Examination pattern model."""
import uuid
from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel


class ExamPattern(Base, BaseModel):
    __tablename__ = "exam_patterns"

    exam_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_questions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    marks_per_correct: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    negative_marking_penalty: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    difficulty_distribution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)

    exam = relationship("Exam", back_populates="patterns")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ExamPattern id={self.id} name={self.name}>"
