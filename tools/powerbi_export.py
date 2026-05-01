"""Helper d'export CSV pour Power BI."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


POWERBI_COLUMNS = [
    "Order ID",
    "Product",
    "Quantity Ordered",
    "Price Each",
    "Order Date",
    "Purchase Address",
    "Sales",
    "City",
    "Hour",
    "Day",
    "Month",
]


def export_clean_sales_for_powerbi(
    cleaned_df: pd.DataFrame,
    output_path: Path | str = "exports/clean_sales_for_powerbi.csv",
) -> Path:
    missing = [column for column in POWERBI_COLUMNS if column not in cleaned_df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes pour l'export Power BI : {', '.join(missing)}")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    export_df = cleaned_df[POWERBI_COLUMNS].copy()
    export_df.to_csv(path, index=False)
    return path
