"""Role endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleOut
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("", response_model=List[RoleOut])
def list_roles(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("administrator")),
):
    return service.roles.get_multi()


@router.post("", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("administrator")),
):
    from app.repositories.role_repository import RoleRepository
    repo = RoleRepository(service.db)
    if repo.get_by_name(role_in.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role already exists")
    role = Role(name=role_in.name, description=role_in.description)
    service.db.add(role)
    service.db.commit()
    service.db.refresh(role)
    return role


@router.get("/{role_id}", response_model=RoleOut)
def get_role(
    role_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("administrator")),
):
    role = service.roles.get(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_roles("administrator")),
):
    service.roles.soft_delete(role_id)
    return None
