import { useEffect, useState } from "react";
import { getToken } from "../auth";
import { healthCheck, runAgent } from "../api";

type Message = { role: "user" | "assistant"; content: string };

export function AIWorkspace() {
  const [provider, setProvider] = useState("mock");
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("Checking API…");

  useEffect(() => { healthCheck().then(() => setStatus("API online")).catch(() => setStatus("API unavailable")); }, []);

  async function send() {
    const token = getToken();
    if (!token || !prompt.trim()) return;
    const text = prompt.trim();
    setPrompt("");
    setMessages((items) => [...items, { role: "user", content: text }]);
    setBusy(true);
    try {
      const result = await runAgent(token, text);
      setMessages((items) => [...items, { role: "assistant", content: result.output }]);
    } catch (error) {
      setMessages((items) => [...items, { role: "assistant", content: error instanceof Error ? error.message : "Request failed" }]);
    } finally { setBusy(false); }
  }

  return <section className="workspace">
    <header className="workspace-header"><div><span className="eyebrow">AI WORKSPACE</span><h2>Jarvis Chat</h2></div><div className="workspace-controls"><span>{status}</span><select value={provider} onChange={(e) => setProvider(e.target.value)}><option value="mock">Mock Provider</option><option value="openai">OpenAI</option></select></div></header>
    <div className="chat-window">{messages.length === 0 && <div className="empty-chat"><strong>Start a conversation</strong><p>Ask Jarvis to plan, write, analyze, or automate something.</p></div>}{messages.map((message, index) => <div key={index} className={`message ${message.role}`}><span>{message.role === "user" ? "YOU" : "JARVIS"}</span><p>{message.content}</p></div>)}</div>
    <div className="composer"><textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); void send(); } }} placeholder="Message Jarvis…" /><button onClick={send} disabled={busy || !prompt.trim()}>{busy ? "…" : "Send →"}</button></div>
  </section>;
}
