"""User schemas."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    display_alias: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    display_alias: Optional[str] = None
    is_active: Optional[bool] = None


class UserWithRoles(UserOut):
    roles: List[str] = []
