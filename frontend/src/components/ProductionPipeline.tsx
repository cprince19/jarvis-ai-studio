import { useState } from "react";
import { getToken } from "../auth";
import { TimelineBuilder, TimelineScene } from "./TimelineBuilder";
import { RenderCenter } from "./RenderCenter";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type Shot = { id?: string; title?: string; duration_seconds?: number; narration?: string; asset_url?: string; captions?: string };

export function ProductionPipeline() {
  const [topic, setTopic] = useState("");
  const [script, setScript] = useState("");
  const [shots, setShots] = useState<Shot[]>([]);
  const [scenes, setScenes] = useState<TimelineScene[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const token = getToken();

  async function generate() {
    if (!token || topic.trim().length < 3) return;
    setBusy(true); setError("");
    try {
      const ai = await fetch(`${API}/api/v1/ai/generate`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ prompt: `Create a YouTube script about: ${topic}`, provider: "mock" }) });
      const aiData = await ai.json();
      if (!ai.ok) throw new Error(aiData.detail || "AI generation failed");
      const generated = aiData.content as string;
      setScript(generated);
      const plan = await fetch(`${API}/api/v1/youtube/production/plan`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, body: JSON.stringify({ script: generated.length >= 20 ? generated : `${generated} ${topic} provides useful context for this production.`, default_duration: 8, voice_id: "default", asset_type: "image", transition: "cut" }) });
      const planData = await plan.json();
      if (!plan.ok) throw new Error(planData.detail || "Production planning failed");
      setShots(planData.shots || []);
      setScenes((planData.shots || []).map((shot: Shot, index: number) => ({ id: shot.id || `shot-${index + 1}`, title: shot.title || `Scene ${index + 1}`, duration_seconds: Number(shot.duration_seconds) || 8, narration: shot.narration || "", media_url: shot.asset_url || "", captions: shot.captions || "" })));
    } catch (e) { setError(e instanceof Error ? e.message : "Production generation failed"); }
    finally { setBusy(false); }
  }

  return <main className="production-pipeline"><header><span className="eyebrow">JARVIS AI STUDIO · PHASE 2</span><h1>YouTube Production</h1><p>Topic → AI → Production Plan → Timeline → Render</p></header><section className="production-input"><input aria-label="YouTube topic" placeholder="Enter a YouTube topic" value={topic} onChange={e => setTopic(e.target.value)} /><button onClick={generate} disabled={busy || topic.trim().length < 3}>{busy ? "Generating…" : "Generate Production"}</button></section>{error && <p role="alert">{error}</p>}{script && <section><h2>Generated Script</h2><textarea value={script} onChange={e => setScript(e.target.value)} /></section>}{shots.length > 0 && <section><h2>Production Plan</h2><p>{shots.length} shots generated.</p></section>}<TimelineBuilder initialScenes={scenes} onChange={setScenes} /><RenderCenter timeline={scenes} /></main>;
}
