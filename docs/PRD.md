# AssessIQ Product Requirements Document

## 1. Product Overview

**Product Name:** AssessIQ  
**Tagline:** Test Your Preparation. Understand Your Performance. Improve Your Potential.  
**Category:** AI-powered competitive examination assessment and performance analytics platform.

### Vision

AssessIQ is a competitive examination assessment platform where students evaluate their preparation through verified question banks, topic-wise assessments, mock examinations, performance analytics, and personalized AI assistance.

Students prepare using external resources such as coaching institutes, textbooks, official documentation, and educational websites. AssessIQ does NOT provide a comprehensive study-material library, coaching courses, or video lessons. Its purpose is to evaluate student knowledge, identify weaknesses, and help students improve examination readiness.

## 2. Core Product Pillars

1. Verified and consistent question bank.
2. Competitive examination assessments.
3. AI-powered performance analysis.
4. Personalized AI assessment tutor.
5. Student progress tracking.
6. Gamification and achievements.

## 3. User Roles

### Student
- Register and authenticate.
- Manage profile.
- Select multiple examinations.
- Explore subjects and topics.
- Attempt mock, topic-wise, subject-wise, previous-year, and custom tests.
- View test results and historical performance.
- Access AI assessment tutor.
- Earn achievements; view leaderboards.
- Track preparation progress.

### Administrator
- Manage examinations, subjects, topics, syllabi, users, source repositories.
- Configure assessment patterns and test series.
- Manage gamification rules.
- Monitor question quality; view system reports.

### Question Reviewer
- Review generated questions; verify correctness.
- Examine source references; review explanations and options.
- Approve, reject, or request corrections.
- Inspect question history.
- Does NOT automatically receive administrator privileges.

### AI Services
- Operate under restricted backend permissions.
- Never approve its own generated questions or publish without human approval.

## 4. Examination Management

- Multiple examinations supported; none hardcoded.
- Administrators add examinations via admin dashboard.
- Hierarchy: Examination → Examination Pattern → Syllabus → Subjects → Topics → Subtopics; plus Test Series and Question Bank.
- Support: reusable subjects, exam-specific subject mapping, hierarchical topics, exam-specific syllabi, configurable marks, negative marking, test duration, question distribution, difficulty distribution, exam status, syllabus versions.

## 5. Question Bank Management

### Categories
1. Historical questions (actual previous-examination questions).
2. AI-generated questions (newly created from verified source material).

AI-generated questions are NEVER labeled as actual previous-year questions.

### Question Attributes
Unique ID, category, exam mapping, subject, topic, subtopic, question text, question type, answer options, correct answer, explanation, difficulty, source references, source evidence location, verification status, reviewer ID, approval timestamp, version number, publication timestamp, active/retired status.

### Question Types (MVP)
- Single-correct-answer MCQ.
- Architecture designed for: multiple-correct MCQ, True/False, Assertion & Reason, Match the Following, Fill in the Blanks.

### Lifecycle
Source Collection → AI Generation → Structured Validation → Duplicate Detection → Answer Verification → Human Review → Reviewer Decision (Reject / Request Correction / Approve) → Publish Question → Question Bank → Assessment Engine. Questions never available to students before approval.

## 6. Source Repository & Verification

- Administrators register source metadata; upload permitted PDFs; store URLs; record publisher, publication date, edition, licensing, chapter/page/section, source versions, mark outdated/disputed sources.
- Every question traceable to source evidence: source ID, title, URL/document ID, page/section, excerpt, retrieval timestamp, source version, verification notes.
- Google searchability is NOT a verification method.
- Verification: factual correctness, exactly one correct option for single-correct MCQs, incorrect options genuinely incorrect, explanation supports answer, source supports claimed answer, flag ambiguous/disputed/conflicting, no fabricated citations.

## 7. AI Question Generation Pipeline

1. Retrieve relevant approved source material.
2. Identify exam, subject, topic.
3. Identify examination patterns.
4. Generate candidate questions, options, correct answer, explanation, source references.
5. Validate structured output (strict Pydantic schemas).
6. Detect duplicates (exact, normalized, trigram, semantic).
7. Evaluate answer evidence.
8. Submit to human review queue.

### Duplicate detection
Exact text matching, normalized text matching, PostgreSQL trigram similarity, semantic similarity via embeddings. Flag candidates for human inspection; do not auto-reject.

## 8. Question Versioning & Immutability (Non-negotiable)

Once published, a question version's text, options, correct answer, explanation, and source evidence cannot be overwritten. Corrections: retire old version, create new version, human approval, publish corrected version, preserve historical version and all previous student attempts. Student answers reference exact question version and option IDs.

## 9. Assessment Engine

### Test types
Topic-wise, subject-wise, full-length mock, previous-year, custom practice, AI-recommended practice.

### Student flow
Select exam → select test type → view instructions → start → answer → navigate → mark for review → autosave → submit → view results/explanations.

### Capabilities
Server-controlled timer, auto-submit on expiry, autosave, recovery after network interruption, question navigation, palette, review flags, randomized question order, randomized option order, negative marking, configurable scoring, submission idempotency, historical attempt integrity. Correct answers never revealed before submission unless configured.

## 10. Performance Analytics

Deterministic Python analytics (no LLM scoring). Calculate: total marks, marks obtained, accuracy, correct/incorrect/unanswered counts, average response time, topic/subject/difficulty accuracy, historical improvement, repeated mistakes, time management. Distinguish marks percentage from answer accuracy. Configurable marking schemes: Score = (Correct × marks per correct) − (Incorrect × negative penalty). Recharts for trends, subject comparison, topic strengths/weaknesses, accuracy over time, test history, time efficiency.

## 11. AI Assessment Assistant

Explain results, identify weak topics, explain incorrect answers, clarify concepts, recommend practice, compare history, explain improvement/decline, encourage constructively. Must retrieve actual student data. Safety: no invented marks/history/sources, no unapproved questions into official tests, grounded explanations, communicate uncertainty, protect PII, rate limits, secure conversation history, RAG protected against prompt injection.

## 12. Gamification

Daily streaks, achievement badges, improvement badges, completion milestones, accuracy milestones, leaderboards, consistency tracking. Leaderboards separated by exam/category. Display aliases. Reward consistency and improvement, not only high marks. Gamification does not alter scoring or correctness.

## 13. Technology Stack

**Frontend:** Next.js App Router, TypeScript strict, Tailwind CSS, shadcn/ui, Lucide icons, Recharts, React Hook Form, Zod, TanStack Query. Server Components by default.

**Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PostgreSQL, JWT, Argon2.

**AI/Data:** Provider-independent LLM service layer, structured JSON outputs, Pydantic validation, RAG, pgvector, Pandas/NumPy, Celery + Redis.

**Testing:** Pytest, HTTPX, Playwright, TypeScript type checking, ESLint, migration checks.

**Infrastructure:** Docker, Docker Compose, env-based config, Git, structured logging.

## 14. Definition of Done (Phase)

A phase is complete only when: backend logic exists, DB operations work, API validated, frontend connected where applicable, authorization enforced, errors handled, tests pass, documentation updated, committed and pushed to GitHub.
