import { useEffect, useState } from "react";
import { getToken } from "../auth";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
type Project = { id:number; topic:string; status:string; title?:string; script?:string; description?:string; tags?:string; research?:string; error?:string };

export function YouTubeEditor({ projectId, onClose }:{projectId:number;onClose:()=>void}) {
  const [project,setProject]=useState<Project|null>(null); const [saving,setSaving]=useState(false); const token=getToken();
  useEffect(()=>{if(!token)return; fetch(`${API}/api/v1/youtube/projects/${projectId}`,{headers:{Authorization:`Bearer ${token}`}}).then(r=>r.ok?r.json():null).then(setProject)},[projectId]);
  if(!project)return <article className="project-detail"><button onClick={onClose}>Close</button><p>Loading project…</p></article>;
  const currentProject = project;
  async function save(){if(!token)return;setSaving(true);try{await fetch(`${API}/api/v1/youtube/projects/${currentProject.id}`,{method:"PATCH",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify({title:currentProject.title,script:currentProject.script,description:currentProject.description,tags:currentProject.tags,research:currentProject.research})});}finally{setSaving(false)}}
  return <article className="youtube-editor"><header><div><span className="eyebrow">CONTENT EDITOR</span><h2>{currentProject.title||currentProject.topic}</h2></div><div><span className={`status ${currentProject.status}`}>{currentProject.status}</span><button onClick={onClose}>Close</button></div></header><label>Research</label><textarea value={currentProject.research||""} onChange={e=>setProject({...currentProject,research:e.target.value})}/><label>Title</label><input value={currentProject.title||""} onChange={e=>setProject({...currentProject,title:e.target.value})}/><label>Script</label><textarea className="script-editor" value={currentProject.script||""} onChange={e=>setProject({...currentProject,script:e.target.value})}/><label>Description</label><textarea value={currentProject.description||""} onChange={e=>setProject({...currentProject,description:e.target.value})}/><label>Tags</label><input value={currentProject.tags||""} onChange={e=>setProject({...currentProject,tags:e.target.value})}/><button onClick={save} disabled={saving}>{saving?"Saving…":"Save Content"}</button></article>;
}
