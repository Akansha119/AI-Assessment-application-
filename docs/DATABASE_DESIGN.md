# AssessIQ Database Design

## 1. Overview

PostgreSQL + SQLAlchemy 2.0 + Alembic. Normalized relational schema. pgvector extension for embeddings/semantic retrieval. All tables include `created_at` and `updated_at` (timestamptz). Soft deletion via `deleted_at` where appropriate. Primary keys: UUID (default `gen_random_uuid()`) or BIGSERIAL as noted.

## 2. Identity

| Table | Purpose |
|-------|---------|
| `roles` | Role definitions (student, administrator, question_reviewer, ai_service) |
| `users` | User accounts (email, argon2 password hash, display alias, active flag) |
| `user_roles` | M:N user ↔ role assignment |
| `user_exams` | M:N user ↔ examination enrollment/selection |

**Key constraints:** `users.email` unique; `roles.name` unique; `user_roles(user_id, role_id)` unique; `user_exams(user_id, exam_id)` unique.

## 3. Examination

| Table | Purpose |
|-------|---------|
| `exams` | Competitive examinations (name, code, status, description) |
| `exam_patterns` | Assessment patterns per exam (marks per correct, negative marking, duration, question count, difficulty distribution) |
| `subjects` | Reusable subjects (name, code) |
| `exam_subjects` | Exam-specific subject mapping (exam_id, subject_id, weightage) |
| `topics` | Hierarchical topics (parent_id self-ref, name, subject_id) |
| `syllabus_versions` | Exam-specific syllabus versions (exam_id, version, effective_from, status) |

**Constraints:** `topics.parent_id` self-FK; `exam_subjects(exam_id, subject_id)` unique; `subjects.code` unique; `exams.code` unique.

## 4. Source Management

| Table | Purpose |
|-------|---------|
| `sources` | Registered source metadata (title, type, publisher, url, publication_date, edition, license, version, active/disputed flag) |
| `source_versions` | Tracked source versions |
| `source_documents` | Uploaded PDF/document files (storage path, mime, size, checksum) |
| `source_chunks` | Extracted text chunks with embeddings (chunk text, page/section, source_id, embedding vector) |

**Constraints:** `source_chunks` pgvector column; GIN/IVFFlat index on embedding for similarity search.

## 5. Questions

| Table | Purpose |
|-------|---------|
| `questions` | Question master (category: historical/ai_generated, exam_id, subject_id, topic_id, subtopic_id, question_type, current_version_id, active/retired) |
| `question_versions` | Immutable version records (question_id, version_number, question_text, correct_answer, explanation, difficulty, approval_status, reviewer_id, approved_at, published_at, is_current) |
| `question_options` | Answer options per version (version_id, option_id, option_text, is_correct, display_order) |
| `question_sources` | Provenance linkage (version_id, source_id, page_section, excerpt, retrieval_timestamp) |
| `question_reviews` | Review decisions (version_id, reviewer_id, decision, notes, reviewed_at) |
| `question_generation_jobs` | AI generation job records (status, prompt, result, created_by) |
| `question_embeddings` | Semantic embeddings per version (version_id, embedding vector) |

**Immutability:** `question_versions` treated as append-only; service enforces no UPDATE on published versions; new version row created for corrections. `question_options.is_correct` cannot change for a published version.

**Constraints:** `question_versions(question_id, version_number)` unique; `question_options(version_id, option_id)` unique; FKs enforce exam/subject/topic chain consistency.

## 6. Assessments

| Table | Purpose |
|-------|---------|
| `tests` | Test configuration (exam_id, title, type, duration, marking scheme, randomization flags, status) |
| `test_questions` | Questions assigned to a test (test_id, question_version_id, display_order, marks) |
| `test_attempts` | Student attempts (test_id, student_id, started_at, submitted_at, status, time_limit_enforced) |
| `student_answers` | Student answers per attempt (attempt_id, question_version_id, option_id, answered_at, time_spent) |
| `test_results` | Computed results (attempt_id, total_marks, marks_obtained, accuracy, correct_count, incorrect_count, unanswered_count, avg_response_time) |

**Constraints:** `student_answers(attempt_id, question_version_id)` unique; submission idempotency enforced at service layer; answers reference exact version + option IDs.

## 7. Analytics

| Table | Purpose |
|-------|---------|
| `topic_performance` | Per student-topic aggregated accuracy |
| `subject_performance` | Per student-subject aggregated accuracy |
| `performance_snapshots` | Periodic performance snapshots for trend analysis |

## 8. AI

| Table | Purpose |
|-------|---------|
| `ai_conversations` | AI tutor conversation sessions (student_id, title) |
| `ai_messages` | Messages (conversation_id, role, content, tokens) |
| `ai_usage_logs` | AI usage for rate limiting/audit (user_id, provider, operation, timestamp) |

## 9. Gamification

| Table | Purpose |
|-------|---------|
| `badges` | Badge definitions (name, criteria, icon) |
| `badge_criteria` | Rule definitions for awarding |
| `badge_awards` | Student badge awards (student_id, badge_id, awarded_at) |
| `streaks` | Practice streaks (student_id, current_streak, last_practice_date) |
| `leaderboard_snapshots` | Cached leaderboard data per exam/category |

## 10. System

| Table | Purpose |
|-------|---------|
| `audit_logs` | Immutable audit trail (actor, action, entity, entity_id, metadata, timestamp) |
| `notifications` | User notifications |
| `system_settings` | Key-value configuration |

## 11. Indexes (selected)

- `users(email)`
- `exams(code)`, `subjects(code)`
- `topics(subject_id)`, `topics(parent_id)`
- `questions(exam_id)`, `questions(subject_id)`, `questions(topic_id)`
- `question_versions(question_id)`, `question_versions(approval_status)`
- `question_options(version_id)`
- `test_attempts(student_id)`, `test_attempts(test_id)`
- `student_answers(attempt_id)`
- `source_chunks` embedding (IVFFlat/HNSW via pgvector)
- `question_embeddings` embedding
- `audit_logs(timestamp)`, `ai_usage_logs(user_id, timestamp)`

## 12. Migration Management

All schema changes via Alembic migrations (`backend/alembic/versions/`). Manual DDL against production is prohibited. Migration autogenerate compared against models in CI.
