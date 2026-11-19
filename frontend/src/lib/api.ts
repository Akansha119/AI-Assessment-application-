export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiError {
  code?: string;
  message?: string;
  details?: unknown;
}

export class AssessIQApiError extends Error {
  status: number;
  code?: string;
  details?: unknown;

  constructor(status: number, message: string, code?: string, details?: unknown) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
    this.name = "AssessIQApiError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = `Request failed: ${response.status}`;
    let code: string | undefined;
    let details: unknown;
    try {
      const body = (await response.json()) as {
        error?: { code?: string; message?: string; details?: unknown };
        detail?: string;
      };
      code = body.error?.code;
      details = body.error?.details || body.detail;
      message = body.error?.message || body.detail || message;
    } catch {
      // ignore parse errors
    }
    throw new AssessIQApiError(response.status, message, code, details);
  }
  if (response.status === 204) {
    return undefined as unknown as T;
  }
  return response.json();
}

export async function apiFetch<T>(
  input: string,
  init?: RequestInit
): Promise<T> {
  const url = input.startsWith("http") ? input : `${API_BASE_URL}${input}`;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };
  const res = await fetch(url, { ...init, headers });
  return handleResponse<T>(res);
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("assessiq_access_token");
}

export function setAccessToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("assessiq_access_token", token);
}

export function removeAccessToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("assessiq_access_token");
}
