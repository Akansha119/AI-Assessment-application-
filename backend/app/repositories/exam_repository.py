"""Exam repository."""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.repositories.base import BaseRepository


class ExamRepository(BaseRepository[Exam]):
    def __init__(self, db: Session):
        super().__init__(Exam, db)

    def get_by_code(self, code: str) -> Optional[Exam]:
        return (
            self.db.query(Exam)
            .filter(Exam.code == code, Exam.deleted_at.is_(None))
            .first()
        )
