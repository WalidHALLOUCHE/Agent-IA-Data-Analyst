"""Génération du rapport Markdown à partir des résultats fiables du pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def build_markdown_report(
    kpis: dict[str, Any],
    quality_report: dict[str, Any],
    insights: dict[str, Any],
    recommendations: dict[str, Any],
) -> str:
    recommendation_lines = "\n".join(
        f"- **{item['category']}**: {item['action']} {item['evidence']}"
        for item in recommendations.get("recommendations", [])
    )
    issue_lines = "\n".join(f"- {issue}" for issue in quality_report.get("issues", []))
    finding_lines = "\n".join(f"- {finding}" for finding in insights.get("key_findings", []))

    return f"""# Rapport Sales Insight AI Agents

## Résumé exécutif

{insights.get("executive_summary", "")}

## Qualité des données

- Lignes brutes : {quality_report.get("raw_rows", 0):,}
- Lignes nettoyées : {quality_report.get("cleaned_rows", 0):,}
- Lignes vides supprimées : {quality_report.get("empty_rows_removed", 0):,}
- En-têtes répétés supprimés : {quality_report.get("repeated_headers_removed", 0):,}
- Lignes invalides supprimées : {quality_report.get("invalid_rows_removed", 0):,}
- Doublons après nettoyage : {quality_report.get("duplicate_rows", 0):,}
- Score qualité : {quality_report.get("quality_score", 0)}/100

### Points de qualité détectés

{issue_lines}

## KPIs

- Chiffre d'affaires total : ${kpis.get("total_revenue", 0):,.2f}
- Commandes uniques : {kpis.get("unique_orders", 0):,}
- Unités vendues : {kpis.get("total_units_sold", 0):,}
- Panier moyen : ${kpis.get("average_order_value", 0):,.2f}
- Prix moyen par ligne : ${kpis.get("average_line_price", 0):,.2f}
- Produit leader en chiffre d'affaires : {kpis.get("top_product_by_revenue", {}).get("name")} (${kpis.get("top_product_by_revenue", {}).get("value", 0):,.2f})
- Produit leader en quantité : {kpis.get("top_product_by_quantity", {}).get("name")} ({kpis.get("top_product_by_quantity", {}).get("value", 0):,.0f} unités)
- Ville leader en chiffre d'affaires : {kpis.get("top_city_by_revenue", {}).get("name")} (${kpis.get("top_city_by_revenue", {}).get("value", 0):,.2f})
- Meilleure heure de vente : {kpis.get("best_sales_hour", {}).get("name")}h (${kpis.get("best_sales_hour", {}).get("value", 0):,.2f})
- Meilleur jour de vente : jour {kpis.get("best_sales_day", {}).get("name")} (${kpis.get("best_sales_day", {}).get("value", 0):,.2f})

## Insights business

{finding_lines}

## Analyse de l'agent IA

{insights.get("ai_narrative", "")}

## Recommandations

{recommendation_lines}

## Limites

- L'analyse repose uniquement sur le CSV de ventes d'avril 2019 fourni.
- Les agents IA ne sont pas autorisés à inventer des métriques ou à utiliser des données externes.
- Les explications business doivent être lues comme des recommandations fondées sur le dataset disponible, pas comme une preuve causale.
"""


def save_markdown_report(report: str, output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    return path
