"""
Argumind AI – Multi-LLM Argument Analysis & Verdict Service.
"""
import asyncio
import logging
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from mistralai import Mistral

from app.core.config import settings

logger = logging.getLogger(__name__)


ANALYST_SYSTEM = """You are a rigorous logical analyst and debate judge.
Your role is to analyse arguments with structured reasoning.
Apply these frameworks:
- Toulmin model (claim, data, warrant, backing, qualifier, rebuttal)
- Logical fallacy identification
- Evidence quality assessment
- Strength-of-argument scoring (0–100)

Always respond in JSON with: {
  "stance": "pro|con|neutral",
  "strength_score": <0-100>,
  "key_claims": [...],
  "evidence_quality": "strong|moderate|weak",
  "logical_fallacies": [...],
  "reasoning_chain": [...],
  "verdict_contribution": "..."
}"""

FEW_SHOT_EXAMPLES = [
    {
        "topic": "Remote work increases productivity",
        "argument": "Studies show 13% productivity boost in remote settings.",
        "expected_stance": "pro",
        "strength_score": 75,
    }
]


class ArgumentAnalysisService:
    def __init__(self):
        self.gpt4 = ChatOpenAI(
            model=settings.GPT4_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        self.claude = ChatAnthropic(
            model=settings.CLAUDE_MODEL,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        self.mistral_client = Mistral(api_key=settings.MISTRAL_API_KEY)

    async def analyse_with_gpt4(self, topic: str, argument: str) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", ANALYST_SYSTEM),
            ("human", f"Topic: {topic}\n\nArgument to analyse:\n{argument}"),
        ])
        response = await self.gpt4.ainvoke(prompt.format_messages())
        return {
            "model": "gpt-4",
            "raw_response": response.content,
            "tokens_used": response.usage_metadata.get("total_tokens", 0) if response.usage_metadata else 0,
        }

    async def analyse_with_claude(self, topic: str, argument: str) -> dict:
        messages = [
            SystemMessage(content=ANALYST_SYSTEM),
            HumanMessage(content=f"Topic: {topic}\n\nArgument to analyse:\n{argument}"),
        ]
        response = await self.claude.ainvoke(messages)
        return {
            "model": "claude",
            "raw_response": response.content,
            "tokens_used": response.usage_metadata.get("total_tokens", 0) if response.usage_metadata else 0,
        }

    async def analyse_with_mistral(self, topic: str, argument: str) -> dict:
        response = self.mistral_client.chat.complete(
            model=settings.MISTRAL_MODEL,
            messages=[
                {"role": "system", "content": ANALYST_SYSTEM},
                {"role": "user", "content": f"Topic: {topic}\n\nArgument to analyse:\n{argument}"},
            ],
        )
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else 0
        return {
            "model": "mistral",
            "raw_response": content,
            "tokens_used": tokens,
        }

    async def full_analysis(self, topic: str, argument: str, models: Optional[list] = None) -> dict:
        if models is None:
            models = ["gpt4", "claude", "mistral"]

        tasks = {}
        if "gpt4" in models:
            tasks["gpt4"] = self.analyse_with_gpt4(topic, argument)
        if "claude" in models:
            tasks["claude"] = self.analyse_with_claude(topic, argument)
        if "mistral" in models:
            tasks["mistral"] = self.analyse_with_mistral(topic, argument)

        results = {}
        for model_name, coro in tasks.items():
            try:
                results[model_name] = await coro
            except Exception as exc:
                logger.error("Error with %s: %s", model_name, exc)
                results[model_name] = {"model": model_name, "error": str(exc)}

        verdict = await self._synthesise_verdict(topic, argument, results)
        return {
            "topic": topic,
            "argument": argument,
            "model_analyses": results,
            "verdict": verdict,
        }

    async def _synthesise_verdict(self, topic: str, argument: str, analyses: dict) -> dict:
        synthesis_prompt = f"""Given these multi-LLM analyses of an argument on '{topic}':

{analyses}

Synthesise a final verdict:
1. Overall argument strength (0-100)
2. Consensus stance across models
3. Key agreements between models
4. Key disagreements
5. Final recommendation

Respond concisely."""
        response = await self.gpt4.ainvoke([HumanMessage(content=synthesis_prompt)])
        return {
            "synthesis": response.content,
            "models_used": list(analyses.keys()),
        }


_service: Optional[ArgumentAnalysisService] = None


def get_argument_service() -> ArgumentAnalysisService:
    global _service
    if _service is None:
        _service = ArgumentAnalysisService()
    return _service
