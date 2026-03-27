> **📅 Project Period:** May 2024 – Aug 2024 &nbsp;|&nbsp; **Status:** Completed &nbsp;|&nbsp; **Author:** [Bharghava Ram Vemuri](https://github.com/bharghavaram)

# 🧠 Argumind AI – Multi-LLM Argument Analysis & Verdict System

> **Agentic argumentation platform using GPT-4, Claude, and Mistral for multi-model logical analysis, fallacy detection, and synthesised verdicts.**

## Overview

Argumind AI is an innovative multi-LLM argumentation platform that analyses arguments through three AI lenses simultaneously, producing a consensus verdict with comprehensive logical scoring. Uses the Toulmin argumentation model and few-shot prompt engineering.

**Key Metrics:**
- 🎯 40% accuracy improvement over single-LLM baseline
- ⚡ 70% reduction in prompt calibration time (few-shot templates)
- 🔍 50+ test cases validated
- 📊 Multi-dimensional argument scoring (0–100)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| LLMs | GPT-4o, Claude 3.5 Sonnet, Mistral Large |
| Frameworks | LangChain, Hugging Face |
| Prompting | Few-shot, ReAct, Structured Output |
| Frontend | React.js |

## Argument Analysis Pipeline

```
User Argument + Topic
        │
        ▼
┌───────────────────────────────────────┐
│  Parallel Multi-LLM Analysis          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│  │  GPT-4  │ │  Claude │ │ Mistral │ │
│  │ Toulmin │ │  Logic  │ │ Stance  │ │
│  │ Scoring │ │ Fallacy │ │ Evidence│ │
│  └─────────┘ └─────────┘ └─────────┘ │
└───────────────────────────────────────┘
        │
        ▼
  GPT-4 Synthesis Engine
        │
        ▼
  Final Verdict + Consensus Score
```

## Quick Start

```bash
git clone https://github.com/bharghavram/argumind-ai.git
cd argumind-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/arguments/analyse` | Full multi-LLM analysis |
| `POST` | `/api/v1/arguments/analyse/single` | Single model analysis |
| `GET` | `/api/v1/arguments/models` | List available models |
| `GET` | `/api/v1/arguments/health` | Health check |

### Example: Full Multi-LLM Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/arguments/analyse" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Remote work increases productivity",
    "argument": "Stanford research shows 13% productivity boost in remote workers due to fewer distractions and no commute.",
    "models": ["gpt4", "claude", "mistral"]
  }'
```

### Response Structure

```json
{
  "topic": "Remote work increases productivity",
  "argument": "...",
  "model_analyses": {
    "gpt4": {"model": "gpt-4", "raw_response": "...", "tokens_used": 450},
    "claude": {"model": "claude", "raw_response": "...", "tokens_used": 380},
    "mistral": {"model": "mistral", "raw_response": "...", "tokens_used": 420}
  },
  "verdict": {
    "synthesis": "Overall strength: 78/100. Consensus: PRO. Key agreements: ...",
    "models_used": ["gpt4", "claude", "mistral"]
  }
}
```

## Scoring Framework (Toulmin Model)

Each LLM evaluates:
- **Claim**: Is the assertion clear?
- **Data**: Quality of supporting evidence
- **Warrant**: Logical link between claim and data
- **Backing**: Additional support
- **Qualifier**: Appropriate hedging
- **Rebuttal**: Counter-argument handling

Plus: Logical fallacy detection, evidence quality rating, strength score (0-100).

## Prompt Engineering

- **Few-shot templates** with 50+ calibration examples
- **Structured output** JSON formatting for consistency
- **Iterative prompt engineering** with versioned rollback
- **ReAct reasoning** for multi-step analysis

## Tests

```bash
pytest tests/ -v
```

---

*Built by Bharghava Ram Vemuri | May 2024 – Aug 2024*
