"""Agent de rapport capable d'améliorer la formulation avec un LLM."""

from __future__ import annotations

import json

from agents.base_ai_agent import BaseAIAgent
from tools.markdown_report import build_markdown_report


class ReportAgent(BaseAIAgent):
    name = "ReportAgent"
    role = "Génère un rapport Markdown complet d'analyse des ventes."

    def run(
        self,
        kpis: dict[str, object],
        quality_report: dict[str, object],
        insights: dict[str, object],
        recommendations: dict[str, object],
    ) -> dict[str, object]:
        deterministic_report = build_markdown_report(kpis, quality_report, insights, recommendations)
        system_prompt = (
            "Tu es un agent IA spécialisé dans le reporting. Réponds en français. Améliore le style "
            "du rapport Markdown en conservant tous les chiffres exactement. N'ajoute pas de métriques, "
            "dates, causes ou affirmations absentes du contexte fiable. Garde les mêmes sections."
        )
        user_prompt = (
            "Réécris ce rapport pour un portfolio GitHub professionnel.\n\n"
            f"Contexte fiable:\n{json.dumps({'kpis': kpis, 'quality': quality_report}, indent=2, default=str)}\n\n"
            f"Brouillon du rapport:\n{deterministic_report}"
        )
        report = self._generate(system_prompt, user_prompt, deterministic_report, max_tokens=1600)
        return {
            "markdown_report": report,
            "used_ai": self.last_used_ai,
            "llm_error": self.last_error,
        }
