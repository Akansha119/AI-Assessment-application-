"""API v1 router aggregation."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, exams, roles, subjects, topics, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
