"""Examination model."""
import uuid
from typing import List, Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel


class Exam(Base, BaseModel):
    __tablename__ = "exams"

    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    enrolled_users: Mapped[List["User"]] = relationship(
        "User", secondary="user_exams", back_populates="enrolled_exams"
    )
    subjects: Mapped[List["ExamSubject"]] = relationship(
        "ExamSubject", foreign_keys="ExamSubject.exam_id", cascade="all, delete-orphan"
    )
    patterns: Mapped[List["ExamPattern"]] = relationship(
        "ExamPattern", foreign_keys="ExamPattern.exam_id", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Exam id={self.id} code={self.code}>"
