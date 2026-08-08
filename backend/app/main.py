from fastapi import FastAPI

from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="Jarvis AI Studio API",
    version="0.1.0",
    description="Foundation API for Jarvis AI Studio.",
)

app.include_router(auth_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jarvis-ai-studio-api", "version": "0.1.0"}


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Jarvis AI Studio API is running"}
