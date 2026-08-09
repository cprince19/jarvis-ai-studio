from celery import shared_task
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.youtube_project import YouTubeProject
from app.youtube.generator import YouTubeContentGenerator


@shared_task(name="jarvis.youtube.generate", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_youtube_project(self, project_id: int, topic: str, audience: str, language: str, tone: str, provider: str = "mock", model: str | None = None) -> dict:
    engine = create_engine(settings.database_url)
    try:
        with Session(engine) as db:
            project = db.get(YouTubeProject, project_id)
            if not project:
                raise ValueError(f"YouTube project {project_id} not found")
            project.status = "running"
            project.error = None
            db.commit()

        import asyncio
        package = asyncio.run(YouTubeContentGenerator().generate(topic, audience, language, tone, provider, model))

        with Session(engine) as db:
            project = db.get(YouTubeProject, project_id)
            if project:
                project.status = "completed"
                project.research = package.research
                project.script = package.script
                project.title = package.title
                project.description = package.description
                project.tags = ",".join(package.tags)
                project.error = None
                db.commit()

        return {"project_id": project_id, "status": "completed"}
    except Exception as exc:
        with Session(engine) as db:
            project = db.get(YouTubeProject, project_id)
            if project:
                project.status = "failed"
                project.error = str(exc)
                db.commit()
        raise
    finally:
        engine.dispose()
