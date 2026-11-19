import { apiFetch } from "@/lib/api";

export interface Exam {
  id: string;
  code: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface ExamCreateInput {
  code: string;
  name: string;
  description?: string;
  is_active?: boolean;
}

export interface ExamUpdateInput {
  name?: string;
  description?: string;
  is_active?: boolean;
}

export interface Subject {
  id: string;
  code: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface SubjectCreateInput {
  code: string;
  name: string;
  description?: string;
}

export interface Topic {
  id: string;
  subject_id: string;
  parent_id: string | null;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface TopicCreateInput {
  subject_id: string;
  parent_id?: string | null;
  name: string;
  description?: string;
}

export interface ExamPattern {
  id: string;
  exam_id: string;
  name: string;
  total_questions: number | null;
  marks_per_correct: number | null;
  negative_marking_penalty: number | null;
  duration_minutes: number | null;
  difficulty_distribution: string | null;
  is_default: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface ExamPatternCreateInput {
  exam_id: string;
  name: string;
  total_questions?: number;
  marks_per_correct?: number;
  negative_marking_penalty?: number;
  duration_minutes?: number;
  difficulty_distribution?: string;
  is_default?: boolean;
}

export interface ExamSubject {
  id: string;
  exam_id: string;
  subject_id: string;
  weightage: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface ExamSubjectCreateInput {
  exam_id: string;
  subject_id: string;
  weightage?: number;
}

export interface SyllabusVersion {
  id: string;
  exam_id: string;
  version: string;
  title: string;
  description: string | null;
  effective_from: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface SyllabusVersionCreateInput {
  exam_id: string;
  version: string;
  title: string;
  description?: string;
  effective_from?: string;
  is_active?: boolean;
}

// Exams
export async function listExams() {
  return apiFetch<Exam[]>("/api/v1/exams");
}

export async function createExam(input: ExamCreateInput) {
  return apiFetch<Exam>("/api/v1/exams", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getExam(id: string) {
  return apiFetch<Exam>(`/api/v1/exams/${id}`);
}

export async function updateExam(id: string, input: ExamUpdateInput) {
  return apiFetch<Exam>(`/api/v1/exams/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteExam(id: string) {
  return apiFetch<void>(`/api/v1/exams/${id}`, { method: "DELETE" });
}

// Subjects
export async function listSubjects() {
  return apiFetch<Subject[]>("/api/v1/subjects");
}

export async function createSubject(input: SubjectCreateInput) {
  return apiFetch<Subject>("/api/v1/subjects", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getSubject(id: string) {
  return apiFetch<Subject>(`/api/v1/subjects/${id}`);
}

// Topics
export async function listTopics(subjectId: string, parentId?: string | null) {
  const params = new URLSearchParams({ subject_id: subjectId });
  if (parentId) params.set("parent_id", parentId);
  return apiFetch<Topic[]>(`/api/v1/topics?${params}`);
}

export async function createTopic(input: TopicCreateInput) {
  return apiFetch<Topic>("/api/v1/topics", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getTopic(id: string) {
  return apiFetch<Topic>(`/api/v1/topics/${id}`);
}

// Exam Patterns
export async function listExamPatterns(examId: string) {
  return apiFetch<ExamPattern[]>(`/api/v1/exam-patterns?exam_id=${examId}`);
}

export async function createExamPattern(input: ExamPatternCreateInput) {
  return apiFetch<ExamPattern>("/api/v1/exam-patterns", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function deleteExamPattern(id: string) {
  return apiFetch<void>(`/api/v1/exam-patterns/${id}`, { method: "DELETE" });
}

// Exam Subjects
export async function listExamSubjects(examId?: string, subjectId?: string) {
  const params = new URLSearchParams();
  if (examId) params.set("exam_id", examId);
  if (subjectId) params.set("subject_id", subjectId);
  return apiFetch<ExamSubject[]>(`/api/v1/exam-subjects?${params}`);
}

export async function createExamSubject(input: ExamSubjectCreateInput) {
  return apiFetch<ExamSubject>("/api/v1/exam-subjects", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function deleteExamSubject(id: string) {
  return apiFetch<void>(`/api/v1/exam-subjects/${id}`, { method: "DELETE" });
}

// Syllabus Versions
export async function listSyllabusVersions(examId: string) {
  return apiFetch<SyllabusVersion[]>(`/api/v1/syllabus-versions?exam_id=${examId}`);
}

export async function createSyllabusVersion(input: SyllabusVersionCreateInput) {
  return apiFetch<SyllabusVersion>("/api/v1/syllabus-versions", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateSyllabusVersion(
  id: string,
  input: SyllabusVersionCreateInput
) {
  return apiFetch<SyllabusVersion>(`/api/v1/syllabus-versions/${id}`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteSyllabusVersion(id: string) {
  return apiFetch<void>(`/api/v1/syllabus-versions/${id}`, { method: "DELETE" });
}
