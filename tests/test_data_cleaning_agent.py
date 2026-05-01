from __future__ import annotations

import pandas as pd

from agents.data_cleaning_agent import DataCleaningAgent


def test_data_cleaning_agent_removes_empty_rows() -> None:
    raw_df = _sample_raw_dataframe(include_empty=True)

    cleaned_df, stats = DataCleaningAgent().run(raw_df)

    assert len(cleaned_df) == 2
    assert stats["empty_rows_removed"] == 1


def test_data_cleaning_agent_removes_repeated_headers() -> None:
    raw_df = _sample_raw_dataframe(include_repeated_header=True)

    cleaned_df, stats = DataCleaningAgent().run(raw_df)

    assert len(cleaned_df) == 2
    assert stats["repeated_headers_removed"] == 1
    assert "Order ID" not in cleaned_df["Order ID"].astype(str).tolist()


def test_data_cleaning_agent_creates_sales_column_correctly() -> None:
    raw_df = _sample_raw_dataframe()

    cleaned_df, _ = DataCleaningAgent().run(raw_df)

    assert "Sales" in cleaned_df.columns
    assert cleaned_df.loc[0, "Sales"] == 23.9
    assert cleaned_df.loc[1, "Sales"] == 99.99


def _sample_raw_dataframe(
    include_empty: bool = False,
    include_repeated_header: bool = False,
) -> pd.DataFrame:
    rows = [
        {
            "Order ID": "176558",
            "Product": "USB-C Charging Cable",
            "Quantity Ordered": "2",
            "Price Each": "11.95",
            "Order Date": "04/19/19 08:46",
            "Purchase Address": "917 1st St, Dallas, TX 75001",
        },
        {
            "Order ID": "176559",
            "Product": "Bose SoundSport Headphones",
            "Quantity Ordered": "1",
            "Price Each": "99.99",
            "Order Date": "04/07/19 22:30",
            "Purchase Address": "682 Chestnut St, Boston, MA 02215",
        },
    ]
    if include_empty:
        rows.insert(1, {column: None for column in rows[0]})
    if include_repeated_header:
        rows.insert(
            1,
            {
                "Order ID": "Order ID",
                "Product": "Product",
                "Quantity Ordered": "Quantity Ordered",
                "Price Each": "Price Each",
                "Order Date": "Order Date",
                "Purchase Address": "Purchase Address",
            },
        )
    return pd.DataFrame(rows)

