"""Role-based permission helpers."""
from typing import Set

ROLE_STUDENT = "student"
ROLE_ADMIN = "administrator"
ROLE_REVIEWER = "question_reviewer"
ROLE_AI_SERVICE = "ai_service"

# Permissions granted to each role (additive; roles stack)
ROLE_PERMISSIONS: dict[str, Set[str]] = {
    ROLE_STUDENT: {
        "exams:read",
        "subjects:read",
        "topics:read",
        "tests:take",
        "results:read_own",
        "ai:chat",
        "gamification:read_own",
    },
    ROLE_REVIEWER: {
        "exams:read",
        "subjects:read",
        "topics:read",
        "questions:review",
        "questions:read_all",
        "question-reviews:decide",
    },
    ROLE_ADMIN: {
        "*",  # admin implies all permissions
    },
    ROLE_AI_SERVICE: {
        "ai:generate",
        "ai:read_usage",
    },
}


def has_permission(user_role_names: Set[str], permission: str) -> bool:
    if ROLE_ADMIN in user_role_names:
        return True
    for role in user_role_names:
        if permission in ROLE_PERMISSIONS.get(role, set()):
            return True
    return False
