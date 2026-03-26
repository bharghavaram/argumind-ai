"""Tests for Argumind AI Argument Analysis Service."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_full_analysis_structure():
    """Full analysis returns expected keys."""
    with patch("app.services.argument_service.ChatOpenAI"), \
         patch("app.services.argument_service.ChatAnthropic"), \
         patch("app.services.argument_service.Mistral"):
        from app.services.argument_service import ArgumentAnalysisService
        svc = ArgumentAnalysisService.__new__(ArgumentAnalysisService)
        svc.gpt4 = AsyncMock()
        svc.gpt4.ainvoke = AsyncMock(return_value=MagicMock(content='{"stance":"pro","strength_score":80}', usage_metadata={}))
        svc.claude = AsyncMock()
        svc.claude.ainvoke = AsyncMock(return_value=MagicMock(content='{"stance":"pro","strength_score":75}', usage_metadata={}))
        svc.mistral_client = MagicMock()
        svc.mistral_client.chat.complete = MagicMock(return_value=MagicMock(
            choices=[MagicMock(message=MagicMock(content='{"stance":"pro","strength_score":78}'))],
            usage=MagicMock(total_tokens=100),
        ))
        result = await svc.full_analysis("AI in healthcare", "AI improves diagnostics.", ["gpt4"])
        assert "topic" in result
        assert "argument" in result
        assert "model_analyses" in result
        assert "verdict" in result


def test_list_models_endpoint():
    """Models endpoint returns three LLMs."""
    from fastapi.testclient import TestClient
    with patch("app.services.argument_service.ChatOpenAI"), \
         patch("app.services.argument_service.ChatAnthropic"), \
         patch("app.services.argument_service.Mistral"):
        from main import app
        client = TestClient(app)
        r = client.get("/api/v1/arguments/models")
        assert r.status_code == 200
        assert len(r.json()["models"]) == 3
