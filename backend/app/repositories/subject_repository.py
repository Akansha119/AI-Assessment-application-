"""Subject repository."""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.repositories.base import BaseRepository


class SubjectRepository(BaseRepository[Subject]):
    def __init__(self, db: Session):
        super().__init__(Subject, db)

    def get_by_code(self, code: str) -> Optional[Subject]:
        return (
            self.db.query(Subject)
            .filter(Subject.code == code, Subject.deleted_at.is_(None))
            .first()
        )
