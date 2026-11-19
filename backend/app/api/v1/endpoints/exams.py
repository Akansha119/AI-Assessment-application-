"""Exam endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.exam import ExamCreate, ExamOut, ExamUpdate
from app.services.exam_service import ExamService

router = APIRouter()


def get_exam_service(db: Session = Depends(get_db)) -> ExamService:
    return ExamService(db)


@router.get("", response_model=List[ExamOut])
def list_exams(
    skip: int = 0,
    limit: int = 100,
    service: ExamService = Depends(get_exam_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_exams(skip=skip, limit=limit)


@router.post("", response_model=ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(
    exam_in: ExamCreate,
    service: ExamService = Depends(get_exam_service),
    current_user: User = Depends(require_roles("administrator")),
):
    try:
        return service.create(exam_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{exam_id}", response_model=ExamOut)
def get_exam(
    exam_id: UUID,
    service: ExamService = Depends(get_exam_service),
    current_user: User = Depends(get_current_user),
):
    exam = service.get(exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam


@router.patch("/{exam_id}", response_model=ExamOut)
def update_exam(
    exam_id: UUID,
    exam_in: ExamUpdate,
    service: ExamService = Depends(get_exam_service),
    current_user: User = Depends(require_roles("administrator")),
):
    exam = service.update(exam_id, exam_in)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_exam(
    exam_id: UUID,
    service: ExamService = Depends(get_exam_service),
    current_user: User = Depends(require_roles("administrator")),
):
    service.deactivate(exam_id)
    return None
