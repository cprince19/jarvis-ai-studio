import { useState } from "react";
import { runAgent } from "../api";
import { clearToken, getToken } from "../auth";

type Props = { onLogout: () => void };

export function Dashboard({ onLogout }: Props) {
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");
  const [busy, setBusy] = useState(false);

  async function execute() {
    const token = getToken();
    if (!token || !prompt.trim()) return;
    setBusy(true);
    try {
      const result = await runAgent(token, prompt.trim());
      setOutput(result.output);
    } catch (error) {
      setOutput(error instanceof Error ? error.message : "Agent execution failed");
    } finally {
      setBusy(false);
    }
  }

  function logout() {
    clearToken();
    onLogout();
  }

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="logo"><span>J</span> Jarvis</div>
        <nav><a className="active">Overview</a><a>AI Agents</a><a>Workflows</a><a>Tasks</a><a>Integrations</a><a>Settings</a></nav>
        <button className="logout" onClick={logout}>Sign out</button>
      </aside>
      <section className="content">
        <header><div><span className="eyebrow">CONTROL CENTER</span><h1>Good to see you.</h1></div><span className="online">● SYSTEM ONLINE</span></header>
        <div className="stats"><article><span>AI Agents</span><strong>1</strong><small>Foundation agent</small></article><article><span>Workflows</span><strong>0</strong><small>Ready to automate</small></article><article><span>Tasks</span><strong>0</strong><small>No queued tasks</small></article></div>
        <section className="agent-panel"><div><span className="eyebrow">JARVIS AGENT</span><h2>What should we build?</h2><p>Test the agent layer before connecting production AI providers.</p></div><textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Ask Jarvis to create a plan, script, workflow, or idea…" /><button onClick={execute} disabled={busy || !prompt.trim()}>{busy ? "Running…" : "Run Agent →"}</button>{output && <div className="output"><span>AGENT OUTPUT</span><p>{output}</p></div>}</section>
      </section>
    </div>
  );
}
