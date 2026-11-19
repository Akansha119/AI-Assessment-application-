"""Syllabus version repository."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.syllabus_version import SyllabusVersion
from app.repositories.base import BaseRepository


class SyllabusVersionRepository(BaseRepository[SyllabusVersion]):
    def __init__(self, db: Session):
        super().__init__(SyllabusVersion, db)

    def get_by_exam(self, exam_id, skip: int = 0, limit: int = 100):
        return (
            self.db.query(SyllabusVersion)
            .filter(
                SyllabusVersion.exam_id == exam_id, SyllabusVersion.deleted_at.is_(None)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
