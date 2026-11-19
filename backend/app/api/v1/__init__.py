"""API v1 router aggregation."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, exams, exam_patterns, exam_subjects, roles, subjects, syllabus_versions, topics, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(exams.router, prefix="/exams", tags=["exams"])
api_router.include_router(exam_patterns.router, prefix="/exam-patterns", tags=["exam-patterns"])
api_router.include_router(exam_subjects.router, prefix="/exam-subjects", tags=["exam-subjects"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(syllabus_versions.router, prefix="/syllabus-versions", tags=["syllabus-versions"])
