"""User service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.roles = RoleRepository(db)

    def get(self, user_id) -> Optional[User]:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.users.get_by_email(email)

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.users.get_multi(skip=skip, limit=limit)

    def update(self, user_id, user_in: UserUpdate) -> Optional[User]:
        user = self.users.get(user_id)
        if not user:
            return None
        data = user_in.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(user, field, value)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate(self, user_id) -> bool:
        return self.users.soft_delete(user_id)

    def assign_role(self, user_id, role_name: str) -> bool:
        user = self.users.get(user_id)
        role = self.roles.get_by_name(role_name)
        if not user or not role:
            return False
        if role in user.roles:
            return True
        user.roles.append(role)
        self.db.add(user)
        self.db.commit()
        return True

    def remove_role(self, user_id, role_name: str) -> bool:
        user = self.users.get(user_id)
        role = self.roles.get_by_name(role_name)
        if not user or not role:
            return False
        user.roles = [r for r in user.roles if r.id != role.id]
        self.db.add(user)
        self.db.commit()
        return True
