import { useEffect, useState } from "react";
import { getToken } from "../auth";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type Project = { id:number; topic:string; status:string; title?:string; script?:string; description?:string; tags?:string; error?:string };

export function YouTubeProjects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selected, setSelected] = useState<Project | null>(null);
  const [topic, setTopic] = useState("");
  const token = getToken();

  async function load() {
    if (!token) return;
    const r = await fetch(`${API}/api/v1/youtube/projects`, { headers:{Authorization:`Bearer ${token}`} });
    if (r.ok) setProjects(await r.json());
  }
  async function create() {
    if (!token || !topic.trim()) return;
    await fetch(`${API}/api/v1/youtube/projects`, { method:"POST", headers:{"Content-Type":"application/json", Authorization:`Bearer ${token}`}, body:JSON.stringify({topic}) });
    setTopic(""); await load();
  }
  async function openProject(id:number) {
    if (!token) return;
    const r = await fetch(`${API}/api/v1/youtube/projects/${id}`, {headers:{Authorization:`Bearer ${token}`}});
    if (r.ok) setSelected(await r.json());
  }
  useEffect(() => { void load(); const timer = window.setInterval(() => void load(), 5000); return () => window.clearInterval(timer); }, []);

  return <section className="youtube-projects">
    <header><div><span className="eyebrow">CONTENT AUTOMATION</span><h2>YouTube Projects</h2></div><div className="project-create"><input value={topic} onChange={e=>setTopic(e.target.value)} placeholder="Enter a video topic…"/><button onClick={create}>Create Project →</button></div></header>
    <div className="project-grid">{projects.map(p=><button className="project-card" key={p.id} onClick={()=>void openProject(p.id)}><span className={`status ${p.status}`}>{p.status}</span><strong>{p.title || p.topic}</strong><small>Project #{p.id}</small></button>)}{projects.length===0 && <div className="empty-projects">No YouTube projects yet.</div>}</div>
    {selected && <article className="project-detail"><button className="close" onClick={()=>setSelected(null)}>Close</button><span className={`status ${selected.status}`}>{selected.status}</span><h3>{selected.title || selected.topic}</h3>{selected.error && <p className="error">{selected.error}</p>}<label>Script</label><textarea value={selected.script || ""} readOnly /><label>Description</label><textarea value={selected.description || ""} readOnly /><label>Tags</label><input value={selected.tags || ""} readOnly /></article>}
  </section>;
}
