# AssessIQ Architecture Document

## 1. Architecture Style

Modular monolith. Frontend and backend are separate applications. No microservices initially.

```
assessiq/
├── frontend/              # Next.js App Router (TypeScript)
├── backend/               # FastAPI (Python 3.12)
├── infrastructure/        # Docker, compose, nginx configs
├── docs/                  # PRD, architecture, DB design, API spec, roadmap, progress
├── scripts/               # seed, dev ops helpers
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 2. Frontend Structure (frontend/src)

```
app/           # App Router routes (Server Components by default)
components/    # shadcn/ui + reusable UI components
features/      # domain feature modules (auth, exams, tests, analytics, ai, gamification)
hooks/         # custom React hooks
lib/           # utilities, API client, validation schemas
services/      # TanStack Query service layer / API bindings
types/         # shared TypeScript types
styles/        # Tailwind globals, design tokens
```

- Server Components default; Client Components only for interaction/browser needs.
- TanStack Query for server-state management.
- React Hook Form + Zod for forms.
- Recharts for analytics.
- Light/dark themes, accessible contrast.

## 3. Backend Structure (backend/app)

```
api/v1/        # versioned REST controllers (thin)
core/          # config, security, logging, dependencies
models/        # SQLAlchemy 2.0 ORM models
schemas/       # Pydantic v2 request/response schemas
repositories/  # data access layer
services/      # business logic (thick)
ai/            # provider-independent LLM service + generation pipeline
analytics/     # deterministic analytics engine
tasks/         # Celery background tasks
permissions/   # RBAC authorization helpers
main.py        # FastAPI application factory
```

- Thin controllers, business logic in services, DB access via repositories.
- Pydantic schemas separate from SQLAlchemy models.
- JWT access + refresh tokens; Argon2 hashing.
- No LLM calls from browser; all AI via backend.
- Structured logging.

## 4. Separation of Concerns

| Layer | Responsibility |
|-------|---------------|
| API controllers | Route requests, parse input, return responses, delegate to services |
| Services | Business rules, transactions, orchestration |
| Repositories | Database queries, SQLAlchemy ORM |
| Models | DB table definitions |
| Schemas | API validation/serialization |

## 5. Security Architecture

- Argon2id password hashing.
- JWT access (short-lived) + refresh tokens.
- Role-based permissions enforced server-side.
- CORS, CSRF (cookie auth), rate limiting, secure file-upload validation.
- Audit logging.
- Secrets in environment variables only; never in frontend env or source control.
- Backend is authority for test timing, answer validation, scoring.
- AI operates under restricted backend permissions; never self-approves.

## 6. Data Flow

### Authentication
Client → API `/api/v1/auth/login` → service verifies Argon2 → issues access + refresh JWT → client stores in httpOnly cookie / memory.

### Test Attempt
Client selects test → server loads questions (answers hidden) → client answers (autosave via API) → server-controlled timer → submit → service computes deterministic score → test_result + student_answers persisted immutably.

### Question Generation
Admin triggers job → Celery task → AI service retrieves approved source chunks (RAG) → generates candidate → Pydantic validation → duplicate detection → human review queue → reviewer approves → published to question bank (immutable version).

### Analytics
Service queries test_results/student_answers → deterministic Python/Pandas computation → frontend Recharts renders.

## 7. Database

PostgreSQL + SQLAlchemy 2.0 + Alembic. pgvector for embeddings. Normalized schema with PK/FK/unique/check constraints, indexes, soft deletion, created/updated timestamps. Immutable published question versions.

## 8. Background Jobs

Celery + Redis for AI question generation, duplicate detection, email/notifications, analytics snapshots.

## 9. Infrastructure

Docker Compose: frontend, backend (FastAPI), PostgreSQL, Redis, Celery worker. Environment-based configuration. Nginx optional reverse proxy.

## 10. Testing Strategy

- Backend: Pytest + HTTPX (unit + integration).
- Frontend: Playwright E2E + Jest/React Testing Library (unit).
- TypeScript type checking (`tsc --noEmit`), ESLint.
- Alembic migration checks (autogenerate comparison).

## 11. Architectural Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| AI self-publishing | Hard backend gate: human review required before publication; AI has no approve permission |
| Question immutability violation | DB constraints/triggers + service-layer enforcement; versioned records |
| Client-trusted scoring | Server recomputes score from stored answers; never trust client-submitted marks/timer |
| Prompt injection via RAG | Sanitize retrieved chunks; system prompt isolation; no raw source content returned to client |
| Secret leakage | .env excluded from git; .env.example only; frontend never holds backend secrets |
