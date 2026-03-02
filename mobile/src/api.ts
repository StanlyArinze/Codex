import { Platform } from "react-native";

const DEFAULT_BASE_URL = Platform.select({
  android: "http://10.0.2.2:8000",
  ios: "http://127.0.0.1:8000",
  default: "http://127.0.0.1:8000"
});

export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? DEFAULT_BASE_URL;
const REQUEST_TIMEOUT_MS = 8000;

type AuthPayload = {
  email: string;
  password: string;
  name?: string;
};

export type AuthResponsePayload = {
  ok: boolean;
  message: string;
  user?: {
    id: number;
    name: string;
  };
};

export type SessionPayload = {
  authenticated: boolean;
  user?: {
    id: number;
    name: string;
  };
};

export type DashboardPayload = {
  period: string;
  summary: {
    income: string;
    expense: string;
    balance: string;
  };
  top_category: string;
  insight: string;
  transactions: Array<{
    date: string;
    description: string;
    category: string;
    type: "income" | "expense";
    amount: string;
  }>;
};

export type CreateTransactionPayload = {
  transaction_type: "income" | "expense";
  amount: string;
  description: string;
  txn_date: string;
};

async function parseJson<T>(response: Response): Promise<T | null> {
  try {
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

async function request(path: string, init?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    return await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      signal: controller.signal
    });
  } finally {
    clearTimeout(timeout);
  }
}

export async function register(payload: AuthPayload): Promise<AuthResponsePayload> {
  const body = new URLSearchParams({
    name: payload.name ?? "",
    email: payload.email,
    password: payload.password
  });

  const response = await request("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    credentials: "include"
  });

  const parsed = await parseJson<AuthResponsePayload>(response);
  return parsed ?? { ok: false, message: "Resposta inválida do servidor." };
}

export async function login(payload: AuthPayload): Promise<AuthResponsePayload> {
  const body = new URLSearchParams({
    email: payload.email,
    password: payload.password
  });

  const response = await request("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    credentials: "include"
  });

  const parsed = await parseJson<AuthResponsePayload>(response);
  return parsed ?? { ok: false, message: "Resposta inválida do servidor." };
}

export async function logout(): Promise<Response> {
  return request("/logout", {
    method: "POST",
    credentials: "include"
  });
}

export async function healthCheck(): Promise<boolean> {
  const response = await request("/api/health", { credentials: "include" });
  const payload = await parseJson<{ status: string }>(response);
  return payload?.status === "ok";
}

export async function fetchSession(): Promise<SessionPayload | null> {
  const response = await request("/api/session", { credentials: "include" });
  return parseJson<SessionPayload>(response);
}

export async function fetchDashboard(period?: string): Promise<DashboardPayload | null> {
  const query = period ? `?period=${period}` : "";
  const response = await request(`/api/dashboard${query}`, { credentials: "include" });
  if (!response.ok) return null;
  return parseJson<DashboardPayload>(response);
}

export async function createTransaction(payload: CreateTransactionPayload): Promise<boolean> {
  const body = new URLSearchParams(payload);
  const response = await request("/api/transactions", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    credentials: "include"
  });
  return response.ok;
}
