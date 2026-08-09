import { useState } from "react";
import { getToken } from "../auth";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type Scene = { number:number; heading:string; narration:string; visual_prompt:string; duration_seconds:number };

export function ScenePlanner({script}:{script:string}) {
  const [scenes,setScenes]=useState<Scene[]>([]); const [busy,setBusy]=useState(false); const [error,setError]=useState("");
  async function plan(){const token=getToken();if(!token)return;setBusy(true);setError("");try{const r=await fetch(`${API}/api/v1/youtube/scenes/plan`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify({script})});if(!r.ok)throw new Error(await r.text());const data=await r.json();setScenes(data.scenes)}catch(e){setError(e instanceof Error?e.message:"Scene planning failed")}finally{setBusy(false)}}
  return <section className="scene-planner"><header><div><span className="eyebrow">PRODUCTION ENGINE</span><h3>Scene Breakdown</h3></div><button onClick={plan} disabled={busy||!script.trim()}>{busy?"Planning…":"Generate Scenes →"}</button></header>{error&&<p className="error">{error}</p>}<div className="scene-list">{scenes.map(s=><article className="scene-card" key={s.number}><span>SCENE {s.number}</span><strong>{s.heading}</strong><p>{s.narration}</p><small>{s.duration_seconds}s · {s.visual_prompt}</small></article>)}</div></section>;
}
