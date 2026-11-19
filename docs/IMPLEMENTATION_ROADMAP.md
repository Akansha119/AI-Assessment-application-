# AssessIQ Implementation Roadmap

## Phase 1 — Foundation (current)
- Inspect repository; initialize Next.js frontend and FastAPI backend.
- Configure PostgreSQL, SQLAlchemy 2.0, Alembic.
- Docker Compose (backend + Postgres + Redis; frontend when Node available).
- Initial database models: identity (users, roles, user_roles, user_exams) and examination (exams, exam_patterns, subjects, exam_subjects, topics, syllabus_versions).
- Authentication (JWT access + refresh, Argon2) and RBAC.
- Run migrations; automated tests for auth and RBAC.

## Phase 2 — Examination Management
- Exam CRUD, subject management, topic hierarchy, syllabus mapping.
- Admin interfaces for examinations/subjects/topics.

## Phase 3 — Question Bank
- Source repository, source chunks, pgvector embeddings.
- Question CRUD, structured schemas, versioning, immutability.
- Human approval workflow, review queue, publication.
- Duplicate detection (exact, normalized, trigram, semantic).

## Phase 4 — Assessment Engine
- Test configuration/creation, question selection.
- Server-controlled timer, autosave, submission idempotency.
- Scoring, result generation, historical attempt integrity.

## Phase 5 — Analytics
- Student dashboard, topic/subject/difficulty performance.
- Historical comparison, time analysis, Recharts frontend.

## Phase 6 — AI Integration
- Provider-independent LLM service layer.
- Source retrieval (RAG), question generation, structured validation.
- Duplicate detection, verification assistance, AI assessment tutor.

## Phase 7 — Gamification
- Badges, streaks, achievements, leaderboards.

## Phase 8 — Quality & Deployment
- Unit/integration tests, Playwright E2E, security checks, performance tests.
- Docker production config, deployment docs.

## Completion Rule
A phase is complete only when implemented, tested, documented, committed, and pushed to GitHub.
