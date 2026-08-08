from fastapi import FastAPI

from app.api.routes.agents import router as agents_router
from app.api.routes.ai import router as ai_router
from app.api.routes.auth import router as auth_router
from app.api.routes.conversations import router as conversations_router
from app.api.routes.executions import router as executions_router
from app.api.routes.users import router as users_router
from app.api.routes.workflows import router as workflows_router

app = FastAPI(
    title="Jarvis AI Studio API",
    version="0.1.0",
    description="Foundation API for Jarvis AI Studio.",
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(workflows_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(conversations_router, prefix="/api/v1")
app.include_router(executions_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jarvis-ai-studio-api", "version": "0.1.0"}


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Jarvis AI Studio API is running"}
