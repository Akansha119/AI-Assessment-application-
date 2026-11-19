"""Exam service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import ExamCreate, ExamUpdate


class ExamService:
    def __init__(self, db: Session):
        self.db = db
        self.exams = ExamRepository(db)

    def create(self, exam_in: ExamCreate) -> Exam:
        if self.exams.get_by_code(exam_in.code):
            raise ValueError("Exam code already exists")
        exam = Exam(**exam_in.model_dump())
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def get(self, exam_id) -> Optional[Exam]:
        return self.exams.get(exam_id)

    def get_by_code(self, code: str) -> Optional[Exam]:
        return self.exams.get_by_code(code)

    def list_exams(self, skip: int = 0, limit: int = 100) -> List[Exam]:
        return self.exams.get_multi(skip=skip, limit=limit)

    def update(self, exam_id, exam_in: ExamUpdate) -> Optional[Exam]:
        exam = self.exams.get(exam_id)
        if not exam:
            return None
        data = exam_in.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(exam, field, value)
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def deactivate(self, exam_id) -> bool:
        return self.exams.soft_delete(exam_id)
