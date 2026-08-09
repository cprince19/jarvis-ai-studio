import json

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.youtube_project import YouTubeProject
from app.tasks.youtube import generate_youtube_project

router = APIRouter(prefix="/youtube/projects", tags=["youtube-projects"])


class ProjectRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    audience: str = Field(default="general audience", max_length=200)
    language: str = Field(default="English", max_length=50)
    tone: str = Field(default="professional and engaging", max_length=100)
    provider: str = "mock"
    model: str | None = None


@router.get("")
def list_projects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(YouTubeProject).where(YouTubeProject.user_id == user.id).order_by(YouTubeProject.created_at.desc())).all()


@router.post("")
def create_project(payload: ProjectRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = YouTubeProject(user_id=user.id, **payload.model_dump(), status="queued")
    db.add(project)
    db.commit()
    db.refresh(project)
    task = generate_youtube_project.delay(project.id, project.topic, project.audience, project.language, project.tone, project.provider, project.model)
    return {"project_id": project.id, "task_id": task.id, "status": project.status}


@router.get("/{project_id}")
def get_project(project_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.scalar(select(YouTubeProject).where(YouTubeProject.id == project_id, YouTubeProject.user_id == user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/tasks/{task_id}")
def get_task(task_id: str, _: User = Depends(get_current_user)):
    result = AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result if result.successful() else None}
