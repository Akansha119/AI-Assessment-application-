"""Exam-subject mapping endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User
from app.schemas.exam_subject import ExamSubjectCreate, ExamSubjectOut
from app.services.exam_subject_service import ExamSubjectService

router = APIRouter()


def get_exam_subject_service(db: Session = Depends(get_db)) -> ExamSubjectService:
    return ExamSubjectService(db)


@router.get("", response_model=List[ExamSubjectOut])
def list_mappings(
    exam_id: UUID | None = None,
    subject_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    service: ExamSubjectService = Depends(get_exam_subject_service),
    current_user: User = Depends(require_roles("administrator")),
):
    if exam_id:
        return service.list_by_exam(exam_id, skip=skip, limit=limit)
    if subject_id:
        return service.list_by_subject(subject_id, skip=skip, limit=limit)
    return []


@router.post("", response_model=ExamSubjectOut, status_code=status.HTTP_201_CREATED)
def create_mapping(
    mapping_in: ExamSubjectCreate,
    service: ExamSubjectService = Depends(get_exam_subject_service),
    current_user: User = Depends(require_roles("administrator")),
):
    try:
        return service.create(mapping_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{mapping_id}", response_model=ExamSubjectOut)
def get_mapping(
    mapping_id: UUID,
    service: ExamSubjectService = Depends(get_exam_subject_service),
    current_user: User = Depends(require_roles("administrator")),
):
    mapping = service.get(mapping_id)
    if not mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
    return mapping


@router.delete("/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_mapping(
    mapping_id: UUID,
    service: ExamSubjectService = Depends(get_exam_subject_service),
    current_user: User = Depends(require_roles("administrator")),
):
    service.deactivate(mapping_id)
    return None
