"""Agent d'insights business avec LLM et fallback déterministe."""

from __future__ import annotations

import json

from agents.base_ai_agent import BaseAIAgent


class BusinessInsightAgent(BaseAIAgent):
    name = "BusinessInsightAgent"
    role = "Transforme les KPI fiables en analyse business exploitable."

    def run(
        self,
        kpis: dict[str, object],
        quality_report: dict[str, object],
    ) -> dict[str, object]:
        fallback_summary = _fallback_summary(kpis, quality_report)
        fallback_findings = _fallback_findings(kpis)
        fallback_text = fallback_summary + "\n\n" + "\n".join(f"- {item}" for item in fallback_findings)

        system_prompt = (
            "Tu es un data analyst e-commerce senior. Réponds en français. Explique uniquement "
            "ce qui est supporté par le JSON fourni. N'invente jamais de chiffres. Si une métrique "
            "manque, indique qu'elle n'est pas disponible. Reste concis et orienté business."
        )
        user_prompt = (
            "Crée un résumé exécutif et des insights business à partir de ce contexte analytique fiable.\n\n"
            f"KPIs:\n{json.dumps(kpis, indent=2, default=str)}\n\n"
            f"Qualité des données:\n{json.dumps(quality_report, indent=2, default=str)}"
        )
        narrative = self._generate(system_prompt, user_prompt, fallback_text, max_tokens=800)

        return {
            "executive_summary": fallback_summary,
            "key_findings": fallback_findings,
            "ai_narrative": narrative,
            "used_ai": self.last_used_ai,
            "llm_error": self.last_error,
        }


def _fallback_summary(kpis: dict[str, object], quality_report: dict[str, object]) -> str:
    return (
        f"Le dataset couvre la période du {kpis.get('period_start')} au {kpis.get('period_end')} "
        f"et génère ${kpis.get('total_revenue', 0):,.2f} de chiffre d'affaires sur "
        f"{kpis.get('unique_orders', 0):,} commandes uniques. Le score de qualité des données est de "
        f"{quality_report.get('quality_score', 0)}/100."
    )


def _fallback_findings(kpis: dict[str, object]) -> list[str]:
    top_product_revenue = kpis.get("top_product_by_revenue", {})
    top_product_quantity = kpis.get("top_product_by_quantity", {})
    top_city = kpis.get("top_city_by_revenue", {})
    best_hour = kpis.get("best_sales_hour", {})
    best_day = kpis.get("best_sales_day", {})
    return [
        f"Produit leader en chiffre d'affaires : {top_product_revenue.get('name')} avec ${top_product_revenue.get('value', 0):,.2f}.",
        f"Produit leader en volume : {top_product_quantity.get('name')} avec {top_product_quantity.get('value', 0):,.0f} unités.",
        f"Ville la plus performante : {top_city.get('name')} avec ${top_city.get('value', 0):,.2f}.",
        f"Meilleure heure de vente : {best_hour.get('name')}h avec ${best_hour.get('value', 0):,.2f}.",
        f"Meilleur jour de vente : jour {best_day.get('name')} avec ${best_day.get('value', 0):,.2f}.",
    ]
