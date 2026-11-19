"""Subject endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.subject import SubjectCreate, SubjectOut
from app.services.subject_service import SubjectService

router = APIRouter()


def get_subject_service(db: Session = Depends(get_db)) -> SubjectService:
    return SubjectService(db)


@router.get("", response_model=List[SubjectOut])
def list_subjects(
    skip: int = 0,
    limit: int = 100,
    service: SubjectService = Depends(get_subject_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_subjects(skip=skip, limit=limit)


@router.post("", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_in: SubjectCreate,
    service: SubjectService = Depends(get_subject_service),
    current_user: User = Depends(require_roles("administrator")),
):
    try:
        return service.create(subject_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(
    subject_id: UUID,
    service: SubjectService = Depends(get_subject_service),
    current_user: User = Depends(get_current_user),
):
    subject = service.get(subject_id)
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return subject
