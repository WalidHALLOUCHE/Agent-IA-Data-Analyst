from __future__ import annotations

import pandas as pd

from agents.data_cleaning_agent import DataCleaningAgent
from agents.data_quality_agent import DataQualityAgent


def test_data_quality_agent_returns_score_between_0_and_100() -> None:
    raw_df = pd.DataFrame(
        [
            {
                "Order ID": "176558",
                "Product": "USB-C Charging Cable",
                "Quantity Ordered": "2",
                "Price Each": "11.95",
                "Order Date": "04/19/19 08:46",
                "Purchase Address": "917 1st St, Dallas, TX 75001",
            },
            {
                "Order ID": None,
                "Product": None,
                "Quantity Ordered": None,
                "Price Each": None,
                "Order Date": None,
                "Purchase Address": None,
            },
        ]
    )
    cleaned_df, stats = DataCleaningAgent().run(raw_df)

    report = DataQualityAgent().run(raw_df, cleaned_df, stats)

    assert 0 <= report["quality_score"] <= 100
    assert report["raw_rows"] == 2
    assert report["cleaned_rows"] == 1

