"""
Argumind AI – Multi-LLM Argument Analysis & Verdict System
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.routes.arguments import router as arguments_router
from app.core.config import settings

app = FastAPI(
    title="Argumind AI – Multi-LLM Argument Analysis",
    description=(
        "Agentic argumentation platform using GPT-4, Claude, and Mistral. "
        "Multi-LLM analysis with iterative prompt engineering, Toulmin model scoring, "
        "logical fallacy detection, and synthesised verdicts."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(arguments_router, prefix="/api/v1")

frontend_path = Path("frontend/dist")
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


@app.get("/api")
async def api_root():
    return {
        "service": "Argumind AI – Multi-LLM Argument Analysis & Verdict System",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "full_analysis": "POST /api/v1/arguments/analyse",
            "single_model": "POST /api/v1/arguments/analyse/single",
            "list_models": "GET /api/v1/arguments/models",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
