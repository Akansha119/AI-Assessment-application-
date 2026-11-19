# AssessIQ

AI-powered competitive examination assessment and performance analytics platform.

**Tagline:** Test Your Preparation. Understand Your Performance. Improve Your Potential.

## Repository Structure

```
assessiq/
├── frontend/          # Next.js App Router (TypeScript, Tailwind, shadcn/ui)
├── backend/           # FastAPI (Python 3.12, SQLAlchemy 2.0, Alembic)
├── infrastructure/    # Docker, compose, nginx
├── docs/              # PRD, architecture, DB design, API spec, roadmap, progress
├── scripts/           # seed and dev helpers
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Technology Stack

**Frontend:** Next.js App Router, TypeScript (strict), Tailwind CSS, shadcn/ui, Lucide icons, Recharts, React Hook Form, Zod, TanStack Query.

**Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL, JWT, Argon2.

**AI/Data:** Provider-independent LLM service layer, structured JSON outputs, RAG, pgvector, Pandas/NumPy, Celery + Redis.

**Testing:** Pytest, HTTPX, Playwright, TypeScript type checking, ESLint.

## Getting Started

### Prerequisites
- Node.js >= 18 (recommended 20 LTS)
- Python 3.12
- PostgreSQL 15+ (or Docker)
- Redis (for Celery)

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # fill in required values
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
cp ../.env.example .env.local   # fill in required values
npm run dev
```

App: http://localhost:3000

### Docker Compose
```bash
docker compose up --build
```

## Environment

See `.env.example` for required variables. Never commit `.env` files or secrets.

## Documentation

- `docs/PRD.md` — product requirements
- `docs/ARCHITECTURE.md` — system architecture
- `docs/DATABASE_DESIGN.md` — schema design
- `docs/API_SPECIFICATION.md` — REST API reference
- `docs/IMPLEMENTATION_ROADMAP.md` — phased delivery plan
- `docs/PROGRESS.md` — development status tracker

## GitHub Workflow

Work is delivered phase by phase. Each phase is implemented, tested, documented, committed, and pushed before the next begins. A phase is complete only when its changes are successfully pushed to the configured GitHub remote.

No `.env`, secrets, or credentials are ever committed.
