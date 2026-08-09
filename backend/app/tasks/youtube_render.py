from app.youtube.render_jobs import RenderJobStore
from app.youtube.render_worker import RenderWorker

# Celery integration point. The application can bind this function to its configured
# Celery instance without making the domain rendering code depend on Celery.

def execute_render_job(job_id: str, clips: list[dict], output_path: str, store: RenderJobStore | None = None):
    worker = RenderWorker(store=store)
    return worker.process(job_id, clips, output_path)
