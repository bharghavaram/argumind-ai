"""Argumind AI – Multi-LLM argument analysis routes."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.services.argument_service import ArgumentAnalysisService, get_argument_service

router = APIRouter(prefix="/arguments", tags=["Argument Analysis"])


class AnalysisRequest(BaseModel):
    topic: str
    argument: str
    models: Optional[List[str]] = None  # ["gpt4", "claude", "mistral"]


class SingleModelRequest(BaseModel):
    topic: str
    argument: str
    model: str = "gpt4"


@router.post("/analyse")
async def analyse_argument(
    request: AnalysisRequest,
    service: ArgumentAnalysisService = Depends(get_argument_service),
):
    """Run full multi-LLM argument analysis with synthesised verdict."""
    if not request.topic.strip() or not request.argument.strip():
        raise HTTPException(status_code=400, detail="Topic and argument must not be empty.")
    result = await service.full_analysis(request.topic, request.argument, request.models)
    return result


@router.post("/analyse/single")
async def analyse_single(
    request: SingleModelRequest,
    service: ArgumentAnalysisService = Depends(get_argument_service),
):
    """Analyse an argument using a single LLM."""
    if request.model == "gpt4":
        return await service.analyse_with_gpt4(request.topic, request.argument)
    elif request.model == "claude":
        return await service.analyse_with_claude(request.topic, request.argument)
    elif request.model == "mistral":
        return await service.analyse_with_mistral(request.topic, request.argument)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}. Use gpt4, claude, or mistral.")


@router.get("/models")
async def list_models():
    """List available LLM models for analysis."""
    return {
        "models": [
            {"id": "gpt4", "name": "GPT-4o", "provider": "OpenAI"},
            {"id": "claude", "name": "Claude 3.5 Sonnet", "provider": "Anthropic"},
            {"id": "mistral", "name": "Mistral Large", "provider": "Mistral AI"},
        ]
    }


@router.get("/health")
async def health():
    return {"status": "ok", "service": "Argumind AI - Multi-LLM Argument Analysis"}
