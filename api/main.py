"""Endpoints FastAPI pour Sales Insight AI Agents."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.llm_client import LLMClient
from agents.orchestrator_agent import OrchestratorAgent
from tools.data_loader import load_default_sales_data


app = FastAPI(
    title="API Sales Insight AI Agents",
    version="1.0.0",
    description="API d'agents IA fiables pour l'analyse de ventes e-commerce.",
)


class QuestionRequest(BaseModel):
    question: str = Field(..., examples=["Quel produit dois-je prioriser ?"])


@app.get("/health", summary="Vérifier l'état de l'API")
def health() -> dict[str, str]:
    return {"status": "OK"}


@app.get("/kpis", summary="Récupérer les KPI")
def get_kpis() -> dict[str, object]:
    result = _run_default_pipeline(ai_enabled=False)
    return result["kpis"]


@app.get("/quality", summary="Récupérer le rapport qualité")
def get_quality() -> dict[str, object]:
    result = _run_default_pipeline(ai_enabled=False)
    return result["quality_report"]


@app.get("/recommendations", summary="Récupérer les recommandations")
def get_recommendations() -> dict[str, object]:
    result = _run_default_pipeline(ai_enabled=True)
    return result["recommendations"]


@app.post("/ask", summary="Poser une question à l'agent IA")
def ask_agent(payload: QuestionRequest) -> dict[str, object]:
    result = _run_default_pipeline(ai_enabled=True)
    answer = OrchestratorAgent(llm_client=LLMClient(enabled=True)).answer(payload.question, result)
    return answer


def _run_default_pipeline(ai_enabled: bool) -> dict[str, object]:
    try:
        raw_df = load_default_sales_data()
        llm_client = LLMClient(enabled=ai_enabled)
        return OrchestratorAgent(llm_client=llm_client).run(raw_df)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
