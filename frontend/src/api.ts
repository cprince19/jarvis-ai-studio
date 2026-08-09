const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) throw new Error((await response.text()) || `Request failed: ${response.status}`);
  return response.json() as Promise<T>;
}

export function healthCheck() { return request<{ status: string; service: string; version: string }>("/health"); }
export function register(email: string, password: string) { return request<{ access_token: string; token_type: string }>("/api/v1/auth/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }) }); }
export function login(email: string, password: string) { return request<{ access_token: string; token_type: string }>("/api/v1/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, password }) }); }
export function runAgent(token: string, prompt: string) { return request<{ output: string; provider: string; model: string }>("/api/v1/agents/run", { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ prompt }) }); }
export function listProviders(token: string) { return request<string[]>("/api/v1/ai/providers", { headers: { Authorization: `Bearer ${token}` } }); }
export function createConversation(token: string, title = "New conversation") { return request<{ id: number; title: string }>("/api/v1/conversations", { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ title }) }); }
export function sendConversationMessage(token: string, conversationId: number, content: string, provider = "mock", model?: string) { return request<{ id: number; role: string; content: string; provider?: string; model?: string }>(`/api/v1/conversations/${conversationId}/messages`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ content, provider, model }) }); }
