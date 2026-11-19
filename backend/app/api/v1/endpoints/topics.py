"""Topic endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicOut
from app.services.topic_service import TopicService

router = APIRouter()


def get_topic_service(db: Session = Depends(get_db)) -> TopicService:
    return TopicService(db)


@router.get("", response_model=List[TopicOut])
def list_topics(
    subject_id: UUID,
    parent_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    service: TopicService = Depends(get_topic_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_topics(
        subject_id=subject_id, parent_id=parent_id, skip=skip, limit=limit
    )


@router.post("", response_model=TopicOut, status_code=status.HTTP_201_CREATED)
def create_topic(
    topic_in: TopicCreate,
    service: TopicService = Depends(get_topic_service),
    current_user: User = Depends(require_roles("administrator")),
):
    topic = service.create(topic_in)
    return topic


@router.get("/{topic_id}", response_model=TopicOut)
def get_topic(
    topic_id: UUID,
    service: TopicService = Depends(get_topic_service),
    current_user: User = Depends(get_current_user),
):
    topic = service.get(topic_id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic
