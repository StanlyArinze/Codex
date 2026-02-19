import { Platform } from "react-native";

const DEFAULT_BASE_URL = Platform.select({
  android: "http://10.0.2.2:8000",
  ios: "http://127.0.0.1:8000",
  default: "http://127.0.0.1:8000"
});

export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? DEFAULT_BASE_URL;

type AuthPayload = {
  email: string;
  password: string;
  name?: string;
};

export async function register(payload: AuthPayload): Promise<Response> {
  const body = new URLSearchParams({
    name: payload.name ?? "",
    email: payload.email,
    password: payload.password
  });

  return fetch(`${API_BASE_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    credentials: "include"
  });
}

export async function login(payload: AuthPayload): Promise<Response> {
  const body = new URLSearchParams({
    email: payload.email,
    password: payload.password
  });

  return fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    credentials: "include"
  });
}

export async function logout(): Promise<Response> {
  return fetch(`${API_BASE_URL}/logout`, {
    method: "POST",
    credentials: "include"
  });
}

export async function fetchHome(): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/`, { credentials: "include" });
  return response.text();
}
