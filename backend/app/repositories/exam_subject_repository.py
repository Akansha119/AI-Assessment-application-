"""Exam-subject repository."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.exam_subject import ExamSubject
from app.repositories.base import BaseRepository


class ExamSubjectRepository(BaseRepository[ExamSubject]):
    def __init__(self, db: Session):
        super().__init__(ExamSubject, db)

    def get_by_exam(self, exam_id, skip: int = 0, limit: int = 100):
        return (
            self.db.query(ExamSubject)
            .filter(ExamSubject.exam_id == exam_id, ExamSubject.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_subject(self, subject_id, skip: int = 0, limit: int = 100):
        return (
            self.db.query(ExamSubject)
            .filter(
                ExamSubject.subject_id == subject_id, ExamSubject.deleted_at.is_(None)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
