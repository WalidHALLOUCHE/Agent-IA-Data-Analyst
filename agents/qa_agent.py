"""Agent de questions-réponses fondé sur le contexte analytique fiable."""

from __future__ import annotations

import json

from agents.base_ai_agent import BaseAIAgent


OUT_OF_SCOPE_MESSAGE = (
    "Je peux répondre uniquement aux questions liées aux ventes, KPI, produits, villes, horaires, "
    "qualité des données, recommandations et rapport généré."
)


class QAAgent(BaseAIAgent):
    name = "QAAgent"
    role = "Répond aux questions en langage naturel à partir des résultats fiables."

    def answer(
        self,
        question: str,
        kpis: dict[str, object],
        quality_report: dict[str, object],
        insights: dict[str, object],
        recommendations: dict[str, object],
    ) -> dict[str, object]:
        if not question.strip():
            return {
                "answer": "Pose une question liée à l'analyse des ventes pour commencer.",
                "used_ai": False,
                "llm_error": None,
            }

        fallback = _fallback_answer(question, kpis, quality_report, insights, recommendations)
        system_prompt = (
            "Tu es un agent data analyst IA fiable. Réponds en français en utilisant uniquement "
            "le contexte JSON fourni. N'invente jamais de chiffres. Si la question sort du périmètre, "
            f"retourne exactement cette phrase : {OUT_OF_SCOPE_MESSAGE}"
        )
        user_prompt = (
            f"Question: {question}\n\n"
            "Contexte fiable:\n"
            f"{json.dumps({'kpis': kpis, 'quality_report': quality_report, 'insights': insights, 'recommendations': recommendations}, indent=2, default=str)}"
        )
        answer = self._generate(system_prompt, user_prompt, fallback, max_tokens=700)
        return {"answer": answer, "used_ai": self.last_used_ai, "llm_error": self.last_error}


def _fallback_answer(
    question: str,
    kpis: dict[str, object],
    quality_report: dict[str, object],
    insights: dict[str, object],
    recommendations: dict[str, object],
) -> str:
    question_lower = question.lower()
    if any(word in question_lower for word in ["revenue", "sales", "ca", "chiffre", "vente", "ventes"]):
        return f"Le chiffre d'affaires total est de ${kpis.get('total_revenue', 0):,.2f}."
    if any(word in question_lower for word in ["product", "produit"]):
        top = kpis.get("top_product_by_revenue", {})
        return f"Le produit leader en chiffre d'affaires est {top.get('name')} avec ${top.get('value', 0):,.2f}."
    if any(word in question_lower for word in ["city", "ville"]):
        city = kpis.get("top_city_by_revenue", {})
        return f"La ville leader en chiffre d'affaires est {city.get('name')} avec ${city.get('value', 0):,.2f}."
    if any(word in question_lower for word in ["hour", "heure"]):
        hour = kpis.get("best_sales_hour", {})
        return f"La meilleure heure de vente est {hour.get('name')}h avec ${hour.get('value', 0):,.2f}."
    if any(word in question_lower for word in ["quality", "qualite", "qualité"]):
        return f"Le score de qualité des données est de {quality_report.get('quality_score', 0)}/100."
    if any(word in question_lower for word in ["recommend", "recommande", "conseil"]):
        items = recommendations.get("recommendations", [])
        return "\n".join(f"- {item['action']} {item['evidence']}" for item in items)
    if any(word in question_lower for word in ["summary", "resume", "résumé", "global"]):
        return str(insights.get("executive_summary", ""))
    return OUT_OF_SCOPE_MESSAGE
