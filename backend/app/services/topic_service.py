"""Topic service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.topic import Topic
from app.repositories.topic_repository import TopicRepository
from app.schemas.topic import TopicCreate


class TopicService:
    def __init__(self, db: Session):
        self.db = db
        self.topics = TopicRepository(db)

    def create(self, topic_in: TopicCreate) -> Topic:
        topic = Topic(**topic_in.model_dump())
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def get(self, topic_id) -> Optional[Topic]:
        return self.topics.get(topic_id)

    def list_topics(
        self, subject_id, parent_id: Optional = None, skip: int = 0, limit: int = 100
    ) -> List[Topic]:
        return self.topics.get_by_subject(
            subject_id, parent_id=parent_id, skip=skip, limit=limit
        )
