"""Exam pattern service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.exam_pattern import ExamPattern
from app.repositories.base import BaseRepository
from app.schemas.exam_pattern import ExamPatternCreate


class ExamPatternService:
    def __init__(self, db: Session):
        self.db = db
        self.patterns = BaseRepository(ExamPattern, db)

    def create(self, pattern_in: ExamPatternCreate) -> ExamPattern:
        pattern = ExamPattern(**pattern_in.model_dump())
        self.db.add(pattern)
        self.db.commit()
        self.db.refresh(pattern)
        return pattern

    def get(self, pattern_id) -> Optional[ExamPattern]:
        return self.patterns.get(pattern_id)

    def list_patterns(
        self, exam_id, skip: int = 0, limit: int = 100
    ) -> List[ExamPattern]:
        return (
            self.db.query(ExamPattern)
            .filter(
                ExamPattern.exam_id == exam_id,
                ExamPattern.deleted_at.is_(None),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, pattern_id, pattern_in) -> Optional[ExamPattern]:
        pattern = self.patterns.get(pattern_id)
        if not pattern:
            return None
        data = pattern_in.model_dump(exclude_unset=True) if hasattr(pattern_in, "model_dump") else dict(pattern_in)
        for field, value in data.items():
            setattr(pattern, field, value)
        self.db.add(pattern)
        self.db.commit()
        self.db.refresh(pattern)
        return pattern

    def deactivate(self, pattern_id) -> bool:
        return self.patterns.soft_delete(pattern_id)
