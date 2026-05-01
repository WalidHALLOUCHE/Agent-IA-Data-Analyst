"""Application Streamlit pour Sales Insight AI Agents."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.llm_client import LLMClient
from agents.orchestrator_agent import OrchestratorAgent
from app.components.charts_view import render_charts
from app.components.kpi_cards import render_kpi_cards
from tools.data_loader import DEFAULT_DATASET_PATH, load_default_sales_data
from tools.powerbi_export import POWERBI_COLUMNS, export_clean_sales_for_powerbi


st.set_page_config(
    page_title="Sales Insight AI Agents",
    layout="wide",
)


def main() -> None:
    st.title("Sales Insight AI Agents")
    st.caption("Mini data analyst IA pour l'analyse des ventes e-commerce")

    with st.sidebar:
        st.header("Jeu de données")
        use_default = st.button("Utiliser le dataset par défaut", use_container_width=True)
        uploaded_file = st.file_uploader("Importer un CSV", type=["csv"])
        ai_enabled = st.toggle("Activer les agents IA", value=True)

    raw_df = _resolve_dataset(uploaded_file, use_default)
    if raw_df is None:
        st.info("Sélectionne le dataset par défaut ou importe un fichier CSV.")
        return

    try:
        result = _run_pipeline(raw_df.to_csv(index=False).encode("utf-8"), ai_enabled)
    except Exception as exc:
        st.error(f"Le pipeline a échoué : {exc}")
        return

    cleaned_df: pd.DataFrame = result["cleaned_dataframe"]
    kpis = result["kpis"]
    quality_report = result["quality_report"]
    insights = result["insights"]
    recommendations = result["recommendations"]
    markdown_report = result["markdown_report"]

    with st.sidebar:
        st.header("Exports")
        if st.button("Exporter le CSV pour Power BI", use_container_width=True):
            export_path = export_clean_sales_for_powerbi(cleaned_df)
            st.success(f"Export généré : {export_path}")
        st.download_button(
            "Télécharger le CSV nettoyé",
            data=cleaned_df[POWERBI_COLUMNS].to_csv(index=False).encode("utf-8"),
            file_name="clean_sales_for_powerbi.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.download_button(
            "Télécharger le rapport Markdown",
            data=markdown_report.encode("utf-8"),
            file_name="sales_insight_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    overview_tab, quality_tab, kpi_tab, agents_tab, report_tab = st.tabs(
        ["Vue d'ensemble", "Qualité des données", "KPI & Graphiques", "Agents IA", "Rapport"]
    )

    with overview_tab:
        _render_overview(raw_df, cleaned_df, kpis)

    with quality_tab:
        _render_quality(quality_report)

    with kpi_tab:
        render_kpi_cards(kpis)
        render_charts(result["chart_data"])

    with agents_tab:
        _render_agents(result, ai_enabled)

    with report_tab:
        st.markdown(markdown_report)


def _resolve_dataset(uploaded_file: object, use_default: bool) -> pd.DataFrame | None:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if use_default or DEFAULT_DATASET_PATH.exists():
        return load_default_sales_data()
    return None


@st.cache_data(show_spinner="Exécution des agents...")
def _run_pipeline(csv_bytes: bytes, ai_enabled: bool) -> dict[str, object]:
    raw_df = pd.read_csv(BytesIO(csv_bytes))
    llm_client = LLMClient(enabled=ai_enabled)
    return OrchestratorAgent(llm_client=llm_client).run(raw_df)


def _render_overview(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, kpis: dict[str, object]) -> None:
    columns = st.columns(4)
    columns[0].metric("Début de période", kpis.get("period_start") or "N/A")
    columns[1].metric("Fin de période", kpis.get("period_end") or "N/A")
    columns[2].metric("Lignes brutes", f"{len(raw_df):,}")
    columns[3].metric("Lignes nettoyées", f"{len(cleaned_df):,}")

    st.subheader("Aperçu des données nettoyées")
    st.dataframe(cleaned_df.head(100), use_container_width=True)

    st.subheader("Colonnes disponibles")
    st.write(", ".join(cleaned_df.columns))


def _render_quality(quality_report: dict[str, object]) -> None:
    columns = st.columns(4)
    columns[0].metric("Score qualité", f"{quality_report.get('quality_score', 0)}/100")
    columns[1].metric("Lignes vides supprimées", f"{quality_report.get('empty_rows_removed', 0):,}")
    columns[2].metric("En-têtes répétés supprimés", f"{quality_report.get('repeated_headers_removed', 0):,}")
    columns[3].metric("Doublons", f"{quality_report.get('duplicate_rows', 0):,}")

    st.subheader("Valeurs manquantes")
    missing_values = pd.DataFrame(
        list(quality_report.get("missing_values", {}).items()),
        columns=["Colonne", "Valeurs manquantes"],
    )
    st.dataframe(missing_values, use_container_width=True)

    st.subheader("Points de qualité détectés")
    for issue in quality_report.get("issues", []):
        st.write(f"- {issue}")


def _render_agents(result: dict[str, object], ai_enabled: bool) -> None:
    st.subheader("Statut des agents")
    statuses = pd.DataFrame(result["agent_statuses"]).rename(
        columns={
            "name": "Agent",
            "role": "Rôle",
            "used_ai": "IA utilisée",
            "error": "Erreur",
        }
    )
    st.dataframe(statuses, use_container_width=True)

    st.subheader("Agent d'insights business")
    st.markdown(result["insights"]["ai_narrative"])

    st.subheader("Agent de recommandations")
    st.markdown(result["recommendations"]["ai_narrative"])

    st.subheader("Poser une question à l'agent QA")
    question = st.text_input("Question", placeholder="Quel produit dois-je prioriser ?")
    if question:
        llm_client = LLMClient(enabled=ai_enabled)
        answer = OrchestratorAgent(llm_client=llm_client).answer(question, result)
        st.write(answer["answer"])
        if answer.get("llm_error") and not answer.get("used_ai"):
            st.caption(f"Mode fallback : {answer['llm_error']}")


if __name__ == "__main__":
    main()
