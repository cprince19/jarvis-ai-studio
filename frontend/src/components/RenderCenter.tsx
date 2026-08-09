import { useEffect, useState } from "react";
import { getToken } from "../auth";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
type Job = { job_id: string; celery_task_id?: string; status: string; progress: number; output_path?: string; error?: string; created_at?: string; started_at?: string; completed_at?: string };

export function RenderCenter({ timeline, onClose }:{timeline: unknown[];onClose?:()=>void}) {
  const [job,setJob]=useState<Job|null>(null); const [starting,setStarting]=useState(false); const token=getToken();
  async function start(){ if(!token)return; setStarting(true); try { const r=await fetch(`${API}/api/v1/youtube/render-jobs`,{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify({timeline})}); const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Unable to start render"); setJob(data); } catch(e){ setJob({job_id:"local-error",status:"FAILED",progress:100,error:e instanceof Error?e.message:"Unable to start render"}); } finally { setStarting(false); } }
  useEffect(()=>{ if(!job?.job_id || job.status==="COMPLETED" || job.status==="FAILED") return; const timer=window.setInterval(async()=>{ const r=await fetch(`${API}/api/v1/youtube/render-jobs/${job.job_id}`,{headers:{Authorization:`Bearer ${token}`}}); if(r.ok)setJob(await r.json()); },1500); return ()=>window.clearInterval(timer); },[job?.job_id,job?.status,token]);
  return <section className="render-center"><header><div><span className="eyebrow">RENDER CENTER</span><h2>Video Production</h2></div>{onClose&&<button onClick={onClose}>Close</button>}</header>{!job?<><p>Ready to render the current timeline.</p><button onClick={start} disabled={starting}>{starting?"Starting…":"Render Video"}</button></>:<><div className="render-status"><strong>{job.status}</strong><span>{job.progress}%</span></div><progress max="100" value={job.progress}/>{job.celery_task_id&&<p>Task: <code>{job.celery_task_id}</code></p>}{job.output_path&&<p>Output: <code>{job.output_path}</code></p>}{job.error&&<p role="alert">{job.error}</p>}{job.status==="FAILED"&&<button onClick={start} disabled={starting}>Retry Render</button>}</>}</section>;
}
