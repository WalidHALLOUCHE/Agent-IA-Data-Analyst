"""Agent d'orchestration principal du workflow d'analyse des ventes."""

from __future__ import annotations

import pandas as pd

from agents.business_insight_agent import BusinessInsightAgent
from agents.chart_agent import ChartAgent
from agents.data_cleaning_agent import DataCleaningAgent
from agents.data_quality_agent import DataQualityAgent
from agents.kpi_agent import KPIAgent
from agents.llm_client import LLMClient
from agents.qa_agent import QAAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_agent import ReportAgent


class OrchestratorAgent:
    name = "OrchestratorAgent"
    role = "Coordonne les outils analytiques et les agents alimentés par LLM."

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.cleaning_agent = DataCleaningAgent()
        self.quality_agent = DataQualityAgent()
        self.kpi_agent = KPIAgent()
        self.chart_agent = ChartAgent()
        self.insight_agent = BusinessInsightAgent(self.llm_client)
        self.recommendation_agent = RecommendationAgent(self.llm_client)
        self.report_agent = ReportAgent(self.llm_client)
        self.qa_agent = QAAgent(self.llm_client)

    def run(self, raw_df: pd.DataFrame) -> dict[str, object]:
        cleaned_df, cleaning_stats = self.cleaning_agent.run(raw_df)
        quality_report = self.quality_agent.run(raw_df, cleaned_df, cleaning_stats)
        kpis = self.kpi_agent.run(cleaned_df)
        chart_data = self.chart_agent.run(cleaned_df)
        insights = self.insight_agent.run(kpis, quality_report)
        recommendations = self.recommendation_agent.run(kpis, quality_report)
        report = self.report_agent.run(kpis, quality_report, insights, recommendations)

        return {
            "raw_shape": raw_df.shape,
            "cleaned_dataframe": cleaned_df,
            "cleaning_stats": cleaning_stats,
            "quality_report": quality_report,
            "kpis": kpis,
            "chart_data": chart_data,
            "insights": insights,
            "recommendations": recommendations,
            "markdown_report": report["markdown_report"],
            "agent_statuses": self.agent_statuses(),
        }

    def answer(self, question: str, pipeline_result: dict[str, object]) -> dict[str, object]:
        return self.qa_agent.answer(
            question=question,
            kpis=pipeline_result["kpis"],
            quality_report=pipeline_result["quality_report"],
            insights=pipeline_result["insights"],
            recommendations=pipeline_result["recommendations"],
        )

    def agent_statuses(self) -> list[dict[str, object]]:
        return [
            {"name": self.cleaning_agent.name, "role": self.cleaning_agent.role, "used_ai": False},
            {"name": self.quality_agent.name, "role": self.quality_agent.role, "used_ai": False},
            {"name": self.kpi_agent.name, "role": self.kpi_agent.role, "used_ai": False},
            {"name": self.chart_agent.name, "role": self.chart_agent.role, "used_ai": False},
            self.insight_agent.status(),
            self.recommendation_agent.status(),
            self.report_agent.status(),
            self.qa_agent.status(),
        ]
