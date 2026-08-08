from celery import Celery

from app.core.config import settings

celery_app = Celery("jarvis", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"], timezone="UTC")


@celery_app.task(name="jarvis.health_check")
def health_check() -> str:
    return "ok"
