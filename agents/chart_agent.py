"""Agent responsable des tables analytiques prêtes pour les graphiques."""

from __future__ import annotations

import pandas as pd

from tools.sales_charts import prepare_chart_data


class ChartAgent:
    name = "ChartAgent"
    role = "Prépare les données de graphiques à partir des résultats fiables."

    def run(self, cleaned_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        return prepare_chart_data(cleaned_df)
