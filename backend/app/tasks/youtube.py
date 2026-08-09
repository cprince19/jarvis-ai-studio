from celery import shared_task

from app.ai.registry import get_provider
from app.youtube.generator import YouTubeContentGenerator


@shared_task(name="jarvis.youtube.generate")
def generate_youtube_project(project_id: int, topic: str, audience: str, language: str, tone: str, provider: str = "mock", model: str | None = None) -> dict:
    """Celery entry point. Database status updates are intentionally handled by the API layer in Phase 1."""
    import asyncio

    package = asyncio.run(YouTubeContentGenerator().generate(topic, audience, language, tone, provider, model))
    return {
        "project_id": project_id,
        "status": "completed",
        "research": package.research,
        "script": package.script,
        "title": package.title,
        "description": package.description,
        "tags": package.tags,
    }
