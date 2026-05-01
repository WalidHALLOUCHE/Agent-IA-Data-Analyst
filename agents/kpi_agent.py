"""Agent responsable du calcul des KPI."""

from __future__ import annotations

import pandas as pd

from tools.sales_kpis import calculate_sales_kpis


class KPIAgent:
    name = "KPIAgent"
    role = "Calcule les KPI fiables à partir du dataframe nettoyé."

    def run(self, cleaned_df: pd.DataFrame) -> dict[str, object]:
        return calculate_sales_kpis(cleaned_df)
