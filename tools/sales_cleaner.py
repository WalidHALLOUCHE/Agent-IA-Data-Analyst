"""Deterministic cleaning logic for raw sales data."""

from __future__ import annotations

from typing import Any

import pandas as pd


REQUIRED_COLUMNS = [
    "Order ID",
    "Product",
    "Quantity Ordered",
    "Price Each",
    "Order Date",
    "Purchase Address",
]


def validate_sales_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Colonnes obligatoires manquantes : {', '.join(missing)}")


def extract_city_state(address: Any) -> str:
    if pd.isna(address):
        return "Unknown"
    parts = [part.strip() for part in str(address).split(",")]
    if len(parts) < 3:
        return "Unknown"
    city = parts[1]
    state = parts[2].split()[0] if parts[2].split() else "Unknown"
    if not city or state == "Unknown":
        return "Unknown"
    return f"{city} ({state})"


def clean_sales_data(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    validate_sales_columns(raw_df)

    df = raw_df.copy()
    raw_rows = int(len(df))

    before_empty = len(df)
    df = df.dropna(how="all")
    empty_rows_removed = int(before_empty - len(df))

    order_id_as_text = df["Order ID"].astype(str).str.strip()
    repeated_header_mask = order_id_as_text.eq("Order ID")
    repeated_headers_removed = int(repeated_header_mask.sum())
    df = df.loc[~repeated_header_mask].copy()

    for column in REQUIRED_COLUMNS:
        if df[column].dtype == "object":
            df[column] = df[column].astype("string").str.strip()
            df[column] = df[column].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    before_conversion = len(df)
    df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"], errors="coerce")
    df["Price Each"] = pd.to_numeric(df["Price Each"], errors="coerce")
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%m/%d/%y %H:%M",
        errors="coerce",
    )

    invalid_mask = (
        df["Order ID"].isna()
        | df["Product"].isna()
        | df["Quantity Ordered"].isna()
        | df["Price Each"].isna()
        | df["Order Date"].isna()
        | df["Purchase Address"].isna()
    )
    df = df.loc[~invalid_mask].copy()
    invalid_rows_removed = int(before_conversion - len(df))

    df["Quantity Ordered"] = df["Quantity Ordered"].astype(int)
    df["Sales"] = df["Quantity Ordered"] * df["Price Each"]
    df["City"] = df["Purchase Address"].apply(extract_city_state)
    df["Hour"] = df["Order Date"].dt.hour.astype(int)
    df["Day"] = df["Order Date"].dt.day.astype(int)
    df["Month"] = df["Order Date"].dt.month.astype(int)
    df = df.reset_index(drop=True)

    stats = {
        "raw_rows": raw_rows,
        "cleaned_rows": int(len(df)),
        "empty_rows_removed": empty_rows_removed,
        "repeated_headers_removed": repeated_headers_removed,
        "invalid_rows_removed": invalid_rows_removed,
        "total_rows_removed": int(raw_rows - len(df)),
    }
    return df, stats
