from __future__ import annotations

import pandas as pd

from agents.data_cleaning_agent import DataCleaningAgent
from agents.kpi_agent import KPIAgent


def test_kpi_agent_calculates_total_revenue() -> None:
    raw_df = pd.DataFrame(
        [
            {
                "Order ID": "1",
                "Product": "Product A",
                "Quantity Ordered": "2",
                "Price Each": "10",
                "Order Date": "04/01/19 10:00",
                "Purchase Address": "1 Main St, Dallas, TX 75001",
            },
            {
                "Order ID": "2",
                "Product": "Product B",
                "Quantity Ordered": "3",
                "Price Each": "20",
                "Order Date": "04/01/19 11:00",
                "Purchase Address": "2 Main St, Boston, MA 02215",
            },
        ]
    )
    cleaned_df, _ = DataCleaningAgent().run(raw_df)

    kpis = KPIAgent().run(cleaned_df)

    assert kpis["total_revenue"] == 80.0
    assert kpis["unique_orders"] == 2
    assert kpis["total_units_sold"] == 5

