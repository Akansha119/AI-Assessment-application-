# AssessIQ API Specification

Base path: `/api/v1`  
Auth: Bearer JWT (access token) + refresh token rotation.  
Content-Type: `application/json`.  
Standard envelope: `{ "data": ..., "meta": {...}, "error": null }` or `{ "data": null, "meta": null, "error": {...} }`.

## 1. Auth — `/api/v1/auth`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/auth/register` | Register new student account | Public |
| POST | `/auth/login` | Authenticate, issue access + refresh tokens | Public |
| POST | `/auth/refresh` | Rotate refresh token, issue new access token | Public (refresh cookie) |
| POST | `/auth/logout` | Invalidate refresh token | Authenticated |
| GET | `/auth/me` | Current user profile | Authenticated |
| PATCH | `/auth/me` | Update own profile | Authenticated (self) |

## 2. Users — `/api/v1/users`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/users` | List users (pagination/filter) | Admin |
| GET | `/users/{id}` | Get user | Admin / self |
| PATCH | `/users/{id}` | Update user | Admin / self (restricted fields) |
| DELETE | `/users/{id}` | Deactivate user | Admin |
| GET | `/users/{id}/roles` | List user roles | Admin |
| POST | `/users/{id}/roles` | Assign role | Admin |
| DELETE | `/users/{id}/roles/{role_id}` | Remove role | Admin |
| GET | `/users/{id}/exams` | List enrolled examinations | Admin / self |
| POST | `/users/{id}/exams` | Enroll in examination | Admin / self |

## 3. Roles — `/api/v1/roles`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/roles` | Admin |
| POST | `/roles` | Admin |
| GET | `/roles/{id}` | Admin |
| PATCH | `/roles/{id}` | Admin |
| DELETE | `/roles/{id}` | Admin |

## 4. Examinations — `/api/v1/exams`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/exams` | List exams (public: active only; admin: all) |
| POST | `/exams` | Create exam | Admin |
| GET | `/exams/{id}` | Get exam |
| PATCH | `/exams/{id}` | Update exam | Admin |
| DELETE | `/exams/{id}` | Delete/retire exam | Admin |
| GET | `/exams/{id}/patterns` | List exam patterns |
| POST | `/exams/{id}/patterns` | Create/update pattern | Admin |

## 5. Subjects — `/api/v1/subjects`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/subjects` | List subjects |
| POST | `/subjects` | Create subject | Admin |
| GET | `/subjects/{id}` | Get subject |
| PATCH | `/subjects/{id}` | Update subject | Admin |
| DELETE | `/subjects/{id}` | Delete subject | Admin |

## 6. Exam-Subjects — `/api/v1/exam-subjects`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/exam-subjects` | List mappings (filter by exam/subject) |
| POST | `/exam-subjects` | Map subject to exam | Admin |
| DELETE | `/exam-subjects/{id}` | Unmap | Admin |

## 7. Topics — `/api/v1/topics`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/topics` | List topics (filter by subject, parent) |
| POST | `/topics` | Create topic | Admin |
| GET | `/topics/{id}` | Get topic |
| PATCH | `/topics/{id}` | Update topic | Admin |
| DELETE | `/topics/{id}` | Delete topic | Admin |
| GET | `/topics/{id}/children` | List subtopics |

## 8. Syllabus Versions — `/api/v1/syllabus-versions`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/syllabus-versions` | List |
| POST | `/syllabus-versions` | Create | Admin |
| GET | `/syllabus-versions/{id}` | Get |
| PATCH | `/syllabus-versions/{id}` | Update | Admin |

## 9. Sources — `/api/v1/sources`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/sources` | List sources |
| POST | `/sources` | Register source | Admin |
| GET | `/sources/{id}` | Get source |
| PATCH | `/sources/{id}` | Update source | Admin |
| DELETE | `/sources/{id}` | Retire source | Admin |
| POST | `/sources/{id}/documents` | Upload document | Admin |
| GET | `/sources/{id}/chunks` | List extracted chunks | Admin / Reviewer |

## 10. Questions — `/api/v1/questions`

Student-facing endpoints EXCLUDE correct answers and explanations before submission.

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/questions` | List published questions (filter/exam/subject/topic/difficulty, pagination) | Student+ |
| GET | `/questions/{id}` | Get published question (no answer key for students) | Student+ |
| POST | `/questions` | Create draft/historical question | Admin |
| PATCH | `/questions/{id}` | Update draft (only non-published versions) | Admin |
| POST | `/questions/{id}/versions` | Create new version | Admin |
| GET | `/questions/{id}/versions` | List versions | Admin / Reviewer |
| GET | `/questions/{id}/sources` | List source provenance | Admin / Reviewer |
| POST | `/questions/{id}/duplicate-check` | Run duplicate detection | Admin |

## 11. Question Reviews — `/api/v1/question-reviews`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/question-reviews` | Review queue (filter by status, exam) | Reviewer / Admin |
| GET | `/question-reviews/{id}` | Review detail | Reviewer / Admin |
| POST | `/question-reviews/{id}/decision` | Approve / Reject / Request Correction | Reviewer |
| GET | `/question-reviews/{id}/history` | Decision history | Reviewer / Admin |

## 12. Tests — `/api/v1/tests`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/tests` | List available tests (student: eligible; admin: all) |
| POST | `/tests` | Create test | Admin |
| GET | `/tests/{id}` | Get test config (questions without answers) | Student (eligible) / Admin |
| PATCH | `/tests/{id}` | Update test | Admin |
| DELETE | `/tests/{id}` | Retire test | Admin |

## 13. Attempts — `/api/v1/attempts`

| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/attempts` | Start attempt (returns attempt_id, questions w/o answers) | Student |
| GET | `/attempts/{id}` | Get attempt state (answers, timer, flags) | Student (owner) / Admin |
| POST | `/attempts/{id}/answers` | Save/autosave an answer (idempotent) | Student (owner) |
| PATCH | `/attempts/{id}/review-flag` | Toggle review flag | Student (owner) |
| POST | `/attempts/{id}/submit` | Submit attempt (server computes score) | Student (owner) |
| GET | `/attempts/{id}/result` | Get result | Student (owner) / Admin |

## 14. Results — `/api/v1/results`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/results` | List own results (pagination/filter) | Student |
| GET | `/results/{id}` | Get detailed result with explanations | Student (owner) / Admin |
| GET | `/results/{id}/analytics` | Topic/subject/difficulty breakdown | Student (owner) / Admin |

## 15. Analytics — `/api/v1/analytics`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/analytics/dashboard` | Student dashboard aggregates | Student |
| GET | `/analytics/topic-performance` | Topic-wise accuracy trend | Student |
| GET | `/analytics/subject-performance` | Subject comparison | Student |
| GET | `/analytics/history` | Historical test history | Student |
| GET | `/analytics/time-efficiency` | Response time analysis | Student |
| GET | `/analytics/reports` | System reports | Admin |

## 16. AI — `/api/v1/ai`

| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/ai/generate-questions` | Trigger AI question generation job | Admin |
| GET | `/ai/generation-jobs/{id}` | Job status/result | Admin |
| POST | `/ai/chat` | AI assessment tutor message | Student |
| GET | `/ai/conversations` | List conversations | Student (owner) |
| GET | `/ai/conversations/{id}/messages` | List messages | Student (owner) |
| GET | `/ai/usage` | Usage logs / rate limit status | Admin / self |

## 17. Gamification — `/api/v1/gamification`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/gamification/badges` | List badges |
| GET | `/gamification/badges/awarded` | My awarded badges | Student |
| GET | `/gamification/streaks` | My streak | Student |
| GET | `/gamification/leaderboards` | Leaderboards (by exam/category) |
| GET | `/gamification/leaderboards/{id}` | Leaderboard detail |

## 18. Admin — `/api/v1/admin`

| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/admin/dashboard` | System dashboard stats | Admin |
| GET | `/admin/audit-logs` | Audit log stream | Admin |
| GET | `/admin/reports` | System reports | Admin |
| GET | `/admin/settings` | System settings | Admin |
| PATCH | `/admin/settings` | Update settings | Admin |

## 19. Error Response

```json
{
  "data": null,
  "meta": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [{"field": "email", "issue": "invalid format"}]
  }
}
```

Standard HTTP status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500.

OpenAPI docs available at `/docs` (Swagger UI) and `/openapi.json`.
