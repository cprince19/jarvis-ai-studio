const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("API health check failed");
  return response.json() as Promise<{ status: string; service: string; version: string }>;
}

export async function register(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new Error("Registration failed");
  return response.json() as Promise<{ access_token: string; token_type: string }>;
}
