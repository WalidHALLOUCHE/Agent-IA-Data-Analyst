"""Agent responsable du nettoyage déterministe des données."""

from __future__ import annotations

import pandas as pd

from tools.sales_cleaner import clean_sales_data


class DataCleaningAgent:
    name = "DataCleaningAgent"
    role = "Nettoie les ventes brutes et crée les colonnes analytiques."

    def run(self, raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
        return clean_sales_data(raw_df)
