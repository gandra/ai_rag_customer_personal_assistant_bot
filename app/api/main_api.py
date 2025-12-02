"""FastAPI entrypoint za rag_customer_personal_assistant_bot."""

from __future__ import annotations

from fastapi import FastAPI

from .routes import router as assistant_router

app = FastAPI(
    title="rag_customer_personal_assistant_bot",
    version="0.1.0",
    description="Customer assistant bot koji kombinuje politike i operativne servise.",
)
app.include_router(assistant_router)


@app.get("/health", tags=["meta"])
async def healthcheck() -> dict[str, str]:
    """Jednostavan health endpoint"""

    return {"status": "ok"}


__all__ = ["app"]
