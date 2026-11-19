"""Syllabus version endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User
from app.schemas.syllabus_version import SyllabusVersionCreate, SyllabusVersionOut
from app.services.syllabus_version_service import SyllabusVersionService

router = APIRouter()


def get_syllabus_service(db: Session = Depends(get_db)) -> SyllabusVersionService:
    return SyllabusVersionService(db)


@router.get("", response_model=List[SyllabusVersionOut])
def list_syllabus_versions(
    exam_id: UUID,
    skip: int = 0,
    limit: int = 100,
    service: SyllabusVersionService = Depends(get_syllabus_service),
    current_user: User = Depends(require_roles("administrator")),
):
    return service.list_by_exam(exam_id=exam_id, skip=skip, limit=limit)


@router.post("", response_model=SyllabusVersionOut, status_code=status.HTTP_201_CREATED)
def create_syllabus_version(
    syllabus_in: SyllabusVersionCreate,
    service: SyllabusVersionService = Depends(get_syllabus_service),
    current_user: User = Depends(require_roles("administrator")),
):
    return service.create(syllabus_in)


@router.get("/{syllabus_id}", response_model=SyllabusVersionOut)
def get_syllabus_version(
    syllabus_id: UUID,
    service: SyllabusVersionService = Depends(get_syllabus_service),
    current_user: User = Depends(require_roles("administrator")),
):
    syllabus = service.get(syllabus_id)
    if not syllabus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Syllabus version not found")
    return syllabus


@router.patch("/{syllabus_id}", response_model=SyllabusVersionOut)
def update_syllabus_version(
    syllabus_id: UUID,
    syllabus_in: SyllabusVersionCreate,
    service: SyllabusVersionService = Depends(get_syllabus_service),
    current_user: User = Depends(require_roles("administrator")),
):
    updated = service.update(syllabus_id, syllabus_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Syllabus version not found")
    return updated


@router.delete("/{syllabus_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_syllabus_version(
    syllabus_id: UUID,
    service: SyllabusVersionService = Depends(get_syllabus_service),
    current_user: User = Depends(require_roles("administrator")),
):
    service.deactivate(syllabus_id)
    return None
