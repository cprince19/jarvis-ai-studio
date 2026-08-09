import { FormEvent, useState } from "react";
import { login, register } from "../api";
import { saveToken } from "../auth";

type Props = { onAuthenticated: () => void };

export function Login({ onAuthenticated }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const result = mode === "login" ? await login(email, password) : await register(email, password);
      saveToken(result.access_token);
      onAuthenticated();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="auth-card" onSubmit={submit}>
      <div className="brand-mark">J</div>
      <span className="eyebrow">JARVIS AI STUDIO</span>
      <h1>{mode === "login" ? "Welcome back" : "Create your workspace"}</h1>
      <p>Build AI agents, workflows, and automation from one studio.</p>
      <label>Email<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></label>
      <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required /></label>
      {error && <div className="error">{error}</div>}
      <button disabled={busy}>{busy ? "Please wait…" : mode === "login" ? "Sign in" : "Create account"}</button>
      <button type="button" className="link-button" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "Create a new account" : "Already have an account? Sign in"}
      </button>
    </form>
  );
}
