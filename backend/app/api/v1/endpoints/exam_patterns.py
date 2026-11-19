"""Exam pattern endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User
from app.schemas.exam_pattern import ExamPatternCreate, ExamPatternOut
from app.services.exam_pattern_service import ExamPatternService

router = APIRouter()


def get_exam_pattern_service(db: Session = Depends(get_db)) -> ExamPatternService:
    return ExamPatternService(db)


@router.get("", response_model=List[ExamPatternOut])
def list_patterns(
    exam_id: UUID,
    skip: int = 0,
    limit: int = 100,
    service: ExamPatternService = Depends(get_exam_pattern_service),
    current_user: User = Depends(require_roles("administrator")),
):
    return service.list_patterns(exam_id=exam_id, skip=skip, limit=limit)


@router.post("", response_model=ExamPatternOut, status_code=status.HTTP_201_CREATED)
def create_pattern(
    pattern_in: ExamPatternCreate,
    service: ExamPatternService = Depends(get_exam_pattern_service),
    current_user: User = Depends(require_roles("administrator")),
):
    return service.create(pattern_in)


@router.get("/{pattern_id}", response_model=ExamPatternOut)
def get_pattern(
    pattern_id: UUID,
    service: ExamPatternService = Depends(get_exam_pattern_service),
    current_user: User = Depends(require_roles("administrator")),
):
    pattern = service.get(pattern_id)
    if not pattern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found")
    return pattern


@router.delete("/{pattern_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_pattern(
    pattern_id: UUID,
    service: ExamPatternService = Depends(get_exam_pattern_service),
    current_user: User = Depends(require_roles("administrator")),
):
    service.deactivate(pattern_id)
    return None
