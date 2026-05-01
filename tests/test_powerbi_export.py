from __future__ import annotations

import pandas as pd

from agents.data_cleaning_agent import DataCleaningAgent
from tools.powerbi_export import POWERBI_COLUMNS, export_clean_sales_for_powerbi


def test_powerbi_export_creates_csv_file(tmp_path) -> None:
    raw_df = pd.DataFrame(
        [
            {
                "Order ID": "1",
                "Product": "Product A",
                "Quantity Ordered": "2",
                "Price Each": "10",
                "Order Date": "04/01/19 10:00",
                "Purchase Address": "1 Main St, Dallas, TX 75001",
            }
        ]
    )
    cleaned_df, _ = DataCleaningAgent().run(raw_df)
    output_path = tmp_path / "clean_sales_for_powerbi.csv"

    exported_path = export_clean_sales_for_powerbi(cleaned_df, output_path)

    assert exported_path.exists()
    exported_df = pd.read_csv(exported_path)
    assert list(exported_df.columns) == POWERBI_COLUMNS

