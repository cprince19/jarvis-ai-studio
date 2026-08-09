from fastapi import APIRouter
from sqlalchemy import text

from app.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.youtube.renderer import FFmpegRenderer

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/readiness")
def readiness() -> dict:
    checks: dict[str, dict] = {}

    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        checks["postgresql"] = {"ready": True}
    except Exception as exc:
        checks["postgresql"] = {"ready": False, "error": str(exc)}

    try:
        with celery_app.connection_for_read() as connection:
            connection.ensure_connection(max_retries=1)
        checks["redis"] = {"ready": True, "broker": settings.REDIS_URL.split("@")[-1]}
    except Exception as exc:
        checks["redis"] = {"ready": False, "error": str(exc)}

    checks["ffmpeg"] = {"ready": FFmpegRenderer().available()}
    ready = all(item.get("ready") for item in checks.values())
    return {"ready": ready, "checks": checks}
