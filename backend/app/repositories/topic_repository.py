"""Topic repository."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.repositories.base import BaseRepository


class TopicRepository(BaseRepository[Topic]):
    def __init__(self, db: Session):
        super().__init__(Topic, db)

    def get_by_subject(
        self, subject_id, parent_id: Optional = None, skip: int = 0, limit: int = 100
    ) -> List[Topic]:
        query = self.db.query(Topic).filter(
            Topic.subject_id == subject_id, Topic.deleted_at.is_(None)
        )
        if parent_id is None:
            query = query.filter(Topic.parent_id.is_(None))
        else:
            query = query.filter(Topic.parent_id == parent_id)
        return query.offset(skip).limit(limit).all()
