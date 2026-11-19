"""Syllabus version service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.syllabus_version import SyllabusVersion
from app.repositories.syllabus_version_repository import SyllabusVersionRepository
from app.schemas.syllabus_version import SyllabusVersionCreate


class SyllabusVersionService:
    def __init__(self, db: Session):
        self.db = db
        self.syllabus_versions = SyllabusVersionRepository(db)

    def create(self, syllabus_in: SyllabusVersionCreate) -> SyllabusVersion:
        syllabus = SyllabusVersion(**syllabus_in.model_dump())
        self.db.add(syllabus)
        self.db.commit()
        self.db.refresh(syllabus)
        return syllabus

    def get(self, syllabus_id) -> Optional[SyllabusVersion]:
        return self.syllabus_versions.get(syllabus_id)

    def list_by_exam(self, exam_id, skip: int = 0, limit: int = 100) -> List[SyllabusVersion]:
        return self.syllabus_versions.get_by_exam(exam_id, skip=skip, limit=limit)

    def update(self, syllabus_id, syllabus_in) -> Optional[SyllabusVersion]:
        syllabus = self.syllabus_versions.get(syllabus_id)
        if not syllabus:
            return None
        data = syllabus_in.model_dump(exclude_unset=True) if hasattr(syllabus_in, "model_dump") else dict(syllabus_in)
        for field, value in data.items():
            setattr(syllabus, field, value)
        self.db.add(syllabus)
        self.db.commit()
        self.db.refresh(syllabus)
        return syllabus

    def deactivate(self, syllabus_id) -> bool:
        return self.syllabus_versions.soft_delete(syllabus_id)
