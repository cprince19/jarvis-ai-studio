import { useEffect, useState } from "react";
import { getToken } from "../auth";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
type Project = { id:number; topic:string; status:string; title?:string; script?:string; description?:string; tags?:string; research?:string; error?:string };

export function YouTubeEditor({ projectId, onClose }:{projectId:number;onClose:()=>void}) {
  const [project,setProject]=useState<Project|null>(null); const [saving,setSaving]=useState(false); const token=getToken();
  useEffect(()=>{if(!token)return; fetch(`${API}/api/v1/youtube/projects/${projectId}`,{headers:{Authorization:`Bearer ${token}`}}).then(r=>r.ok?r.json():null).then(setProject)},[projectId]);
  if(!project)return <article className="project-detail"><button onClick={onClose}>Close</button><p>Loading project…</p></article>;
  async function save(){if(!token)return;setSaving(true);try{await fetch(`${API}/api/v1/youtube/projects/${project.id}`,{method:"PATCH",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify({title:project.title,script:project.script,description:project.description,tags:project.tags,research:project.research})});}finally{setSaving(false)}}
  return <article className="youtube-editor"><header><div><span className="eyebrow">CONTENT EDITOR</span><h2>{project.title||project.topic}</h2></div><div><span className={`status ${project.status}`}>{project.status}</span><button onClick={onClose}>Close</button></div></header><label>Research</label><textarea value={project.research||""} onChange={e=>setProject({...project,research:e.target.value})}/><label>Title</label><input value={project.title||""} onChange={e=>setProject({...project,title:e.target.value})}/><label>Script</label><textarea className="script-editor" value={project.script||""} onChange={e=>setProject({...project,script:e.target.value})}/><label>Description</label><textarea value={project.description||""} onChange={e=>setProject({...project,description:e.target.value})}/><label>Tags</label><input value={project.tags||""} onChange={e=>setProject({...project,tags:e.target.value})}/><button onClick={save} disabled={saving}>{saving?"Saving…":"Save Content"}</button></article>;
}
