"""Exam-subject service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.exam_subject import ExamSubject
from app.repositories.exam_subject_repository import ExamSubjectRepository
from app.schemas.exam_subject import ExamSubjectCreate


class ExamSubjectService:
    def __init__(self, db: Session):
        self.db = db
        self.exam_subjects = ExamSubjectRepository(db)

    def create(self, mapping_in: ExamSubjectCreate) -> ExamSubject:
        existing = (
            self.db.query(ExamSubject)
            .filter(
                ExamSubject.exam_id == mapping_in.exam_id,
                ExamSubject.subject_id == mapping_in.subject_id,
                ExamSubject.deleted_at.is_(None),
            )
            .first()
        )
        if existing:
            raise ValueError("Subject already mapped to this exam")
        mapping = ExamSubject(**mapping_in.model_dump())
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def get(self, mapping_id) -> Optional[ExamSubject]:
        return self.exam_subjects.get(mapping_id)

    def list_by_exam(self, exam_id, skip: int = 0, limit: int = 100) -> List[ExamSubject]:
        return self.exam_subjects.get_by_exam(exam_id, skip=skip, limit=limit)

    def list_by_subject(self, subject_id, skip: int = 0, limit: int = 100) -> List[ExamSubject]:
        return self.exam_subjects.get_by_subject(subject_id, skip=skip, limit=limit)

    def deactivate(self, mapping_id) -> bool:
        return self.exam_subjects.soft_delete(mapping_id)
