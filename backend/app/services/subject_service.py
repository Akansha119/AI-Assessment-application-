"""Subject service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.repositories.subject_repository import SubjectRepository
from app.schemas.subject import SubjectCreate


class SubjectService:
    def __init__(self, db: Session):
        self.db = db
        self.subjects = SubjectRepository(db)

    def create(self, subject_in: SubjectCreate) -> Subject:
        if self.subjects.get_by_code(subject_in.code):
            raise ValueError("Subject code already exists")
        subject = Subject(**subject_in.model_dump())
        self.db.add(subject)
        self.db.commit()
        self.db.refresh(subject)
        return subject

    def get(self, subject_id) -> Optional[Subject]:
        return self.subjects.get(subject_id)

    def get_by_code(self, code: str) -> Optional[Subject]:
        return self.subjects.get_by_code(code)

    def list_subjects(self, skip: int = 0, limit: int = 100) -> List[Subject]:
        return self.subjects.get_multi(skip=skip, limit=limit)
