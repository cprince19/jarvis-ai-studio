"""Lightweight runtime verification helper.

Run inside the backend container after the stack is up:
    python scripts/verify_render_pipeline.py

This deliberately performs only connectivity checks; it does not create or
modify production data.
"""

from sqlalchemy import text

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.youtube.renderer import FFmpegRenderer


def main() -> int:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    print("PostgreSQL: OK")

    with celery_app.connection_for_read() as connection:
        connection.ensure_connection(max_retries=1)
    print("Redis: OK")

    if not FFmpegRenderer().available():
        print("FFmpeg: NOT AVAILABLE")
        return 1
    print("FFmpeg: OK")
    print("Runtime dependencies: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
