"""Sales KPI calculations.

All business numbers are calculated from the cleaned dataframe.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def calculate_sales_kpis(cleaned_df: pd.DataFrame) -> dict[str, Any]:
    if cleaned_df.empty:
        return _empty_kpis()

    total_revenue = float(cleaned_df["Sales"].sum())
    unique_orders = int(cleaned_df["Order ID"].nunique())
    total_units_sold = int(cleaned_df["Quantity Ordered"].sum())
    average_order_value = float(total_revenue / unique_orders) if unique_orders else 0.0
    average_line_price = float(cleaned_df["Price Each"].mean())

    product_revenue = _top_group(cleaned_df, "Product", "Sales")
    product_quantity = _top_group(cleaned_df, "Product", "Quantity Ordered")
    city_revenue = _top_group(cleaned_df, "City", "Sales")
    hour_revenue = _top_group(cleaned_df, "Hour", "Sales")
    day_revenue = _top_group(cleaned_df, "Day", "Sales")

    return {
        "total_revenue": round(total_revenue, 2),
        "unique_orders": unique_orders,
        "total_units_sold": total_units_sold,
        "average_order_value": round(average_order_value, 2),
        "average_line_price": round(average_line_price, 2),
        "top_product_by_revenue": product_revenue,
        "top_product_by_quantity": product_quantity,
        "top_city_by_revenue": city_revenue,
        "best_sales_hour": hour_revenue,
        "best_sales_day": day_revenue,
        "period_start": cleaned_df["Order Date"].min().strftime("%Y-%m-%d %H:%M"),
        "period_end": cleaned_df["Order Date"].max().strftime("%Y-%m-%d %H:%M"),
    }


def _top_group(df: pd.DataFrame, group_column: str, value_column: str) -> dict[str, Any]:
    grouped = (
        df.groupby(group_column, dropna=False)[value_column]
        .sum()
        .sort_values(ascending=False)
    )
    if grouped.empty:
        return {"name": None, "value": 0}
    name = grouped.index[0]
    value = grouped.iloc[0]
    if hasattr(name, "item"):
        name = name.item()
    return {"name": name, "value": round(float(value), 2)}


def _empty_kpis() -> dict[str, Any]:
    empty_top = {"name": None, "value": 0}
    return {
        "total_revenue": 0.0,
        "unique_orders": 0,
        "total_units_sold": 0,
        "average_order_value": 0.0,
        "average_line_price": 0.0,
        "top_product_by_revenue": empty_top,
        "top_product_by_quantity": empty_top,
        "top_city_by_revenue": empty_top,
        "best_sales_hour": empty_top,
        "best_sales_day": empty_top,
        "period_start": None,
        "period_end": None,
    }

