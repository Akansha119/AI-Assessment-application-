"""Base repository with common CRUD operations."""
from datetime import datetime, timezone
from uuid import UUID
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def _coerce_id(self, id):
        try:
            return UUID(str(id))
        except (ValueError, AttributeError, TypeError):
            return id

    def get(self, id) -> ModelType | None:
        id = self._coerce_id(id)
        return self.db.query(self.model).filter(
            self.model.id == id, self.model.deleted_at.is_(None)
        ).first()

    def get_multi(self, skip: int = 0, limit: int = 100):
        return (
            self.db.query(self.model)
            .filter(self.model.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj_in) -> ModelType:
        data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else dict(obj_in)
        db_obj = self.model(**data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def soft_delete(self, id) -> bool:
        obj = self.get(id)
        if obj is None:
            return False
        obj.deleted_at = datetime.now(timezone.utc)
        self.db.add(obj)
        self.db.commit()
        return True
