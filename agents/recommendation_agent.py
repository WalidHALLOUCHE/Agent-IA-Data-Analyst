"""Agent de recommandations avec LLM et preuves déterministes."""

from __future__ import annotations

import json

from agents.base_ai_agent import BaseAIAgent


class RecommendationAgent(BaseAIAgent):
    name = "RecommendationAgent"
    role = "Produit des recommandations business reliées aux KPI fiables."

    def run(
        self,
        kpis: dict[str, object],
        quality_report: dict[str, object],
    ) -> dict[str, object]:
        recommendations = _deterministic_recommendations(kpis, quality_report)
        fallback = "\n".join(
            f"- {item['category']} : {item['action']} Preuve : {item['evidence']}"
            for item in recommendations
        )
        system_prompt = (
            "Tu es un consultant business IA. Réponds en français. Reformule les recommandations "
            "dans un style clair et professionnel. Utilise uniquement les preuves fournies. "
            "N'ajoute pas de métriques, estimations, causes ou hypothèses."
        )
        user_prompt = (
            "Améliore la formulation de ces recommandations en conservant exactement chaque chiffre.\n\n"
            f"Recommandations:\n{json.dumps(recommendations, indent=2, default=str)}"
        )
        narrative = self._generate(system_prompt, user_prompt, fallback, max_tokens=800)
        return {
            "recommendations": recommendations,
            "ai_narrative": narrative,
            "used_ai": self.last_used_ai,
            "llm_error": self.last_error,
        }


def _deterministic_recommendations(
    kpis: dict[str, object],
    quality_report: dict[str, object],
) -> list[dict[str, str]]:
    top_product_revenue = kpis.get("top_product_by_revenue", {})
    top_product_quantity = kpis.get("top_product_by_quantity", {})
    top_city = kpis.get("top_city_by_revenue", {})
    best_hour = kpis.get("best_sales_hour", {})
    score = quality_report.get("quality_score", 0)

    return [
        {
            "category": "Marketing",
            "action": f"Prioriser les campagnes autour de {top_product_revenue.get('name')}.",
            "evidence": f"Ce produit génère le chiffre d'affaires le plus élevé avec ${top_product_revenue.get('value', 0):,.2f}.",
        },
        {
            "category": "Produit",
            "action": f"Sécuriser le stock de {top_product_quantity.get('name')}.",
            "evidence": f"Ce produit affiche le plus gros volume avec {top_product_quantity.get('value', 0):,.0f} unités vendues.",
        },
        {
            "category": "Zone géographique",
            "action": f"Analyser {top_city.get('name')} comme marché prioritaire.",
            "evidence": f"Cette ville génère le chiffre d'affaires le plus élevé avec ${top_city.get('value', 0):,.2f}.",
        },
        {
            "category": "Timing",
            "action": f"Planifier les contrôles promotionnels autour de {best_hour.get('name')}h.",
            "evidence": f"Cette heure génère le chiffre d'affaires le plus élevé avec ${best_hour.get('value', 0):,.2f}.",
        },
        {
            "category": "Qualité des données",
            "action": "Conserver les contrôles d'en-têtes répétés et de lignes invalides dans le pipeline d'ingestion.",
            "evidence": f"Le score de qualité actuel est de {score}/100.",
        },
    ]
