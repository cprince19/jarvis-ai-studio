import { useMemo, useState } from "react";

export type TimelineScene = {
  id: string;
  title: string;
  duration_seconds: number;
  narration?: string;
  media_url?: string;
  captions?: string;
};

export function TimelineBuilder({ initialScenes = [], onChange }:{initialScenes?:TimelineScene[];onChange?:(scenes:TimelineScene[])=>void}) {
  const [scenes,setScenes]=useState<TimelineScene[]>(initialScenes);
  const total=useMemo(()=>scenes.reduce((sum,s)=>sum+s.duration_seconds,0),[scenes]);
  function update(id:string, patch:Partial<TimelineScene>){const next=scenes.map(s=>s.id===id?{...s,...patch}:s);setScenes(next);onChange?.(next)}
  function add(){const next=[...scenes,{id:crypto.randomUUID(),title:`Scene ${scenes.length+1}`,duration_seconds:5,narration:""}];setScenes(next);onChange?.(next)}
  function remove(id:string){const next=scenes.filter(s=>s.id!==id);setScenes(next);onChange?.(next)}
  return <section className="timeline-builder"><header><div><span className="eyebrow">TIMELINE</span><h2>Scene Builder</h2></div><strong>{total}s</strong></header>{scenes.map((scene,index)=><article className="timeline-scene" key={scene.id}><header><span>#{index+1}</span><button onClick={()=>remove(scene.id)}>Remove</button></header><input aria-label={`Scene ${index+1} title`} value={scene.title} onChange={e=>update(scene.id,{title:e.target.value})}/><input aria-label={`Scene ${index+1} duration`} type="number" min="1" step="1" value={scene.duration_seconds} onChange={e=>update(scene.id,{duration_seconds:Math.max(1,Number(e.target.value)||1)})}/><textarea aria-label={`Scene ${index+1} narration`} value={scene.narration||""} onChange={e=>update(scene.id,{narration:e.target.value})}/><input aria-label={`Scene ${index+1} media URL`} placeholder="Media URL" value={scene.media_url||""} onChange={e=>update(scene.id,{media_url:e.target.value})}/><textarea aria-label={`Scene ${index+1} captions`} placeholder="Captions" value={scene.captions||""} onChange={e=>update(scene.id,{captions:e.target.value})}/></article>)}<button onClick={add}>Add Scene</button></section>;
}
