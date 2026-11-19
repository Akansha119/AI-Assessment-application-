"""Exam-subject mapping model."""
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel


class ExamSubject(Base, BaseModel):
    __tablename__ = "exam_subjects"

    exam_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    weightage: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)

    exam = relationship("Exam", back_populates="subjects")
    subject = relationship("Subject", back_populates="exam_mappings")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ExamSubject exam_id={self.exam_id} subject_id={self.subject_id}>"
