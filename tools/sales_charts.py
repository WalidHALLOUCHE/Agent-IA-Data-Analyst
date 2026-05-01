"""Préparation des données graphiques et figures Plotly."""

from __future__ import annotations

import pandas as pd


def prepare_chart_data(cleaned_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "top_products_revenue": _group_sum(cleaned_df, "Product", "Sales", 10),
        "top_products_quantity": _group_sum(cleaned_df, "Product", "Quantity Ordered", 10),
        "sales_by_city": _group_sum(cleaned_df, "City", "Sales", 20),
        "sales_by_hour": _group_sum(cleaned_df, "Hour", "Sales", None).sort_values("Hour"),
        "sales_by_day": _group_sum(cleaned_df, "Day", "Sales", None).sort_values("Day"),
        "sales_distribution": cleaned_df[["Sales"]].copy(),
    }


def build_sales_figures(chart_data: dict[str, pd.DataFrame]) -> dict[str, object]:
    import plotly.express as px

    return {
        "top_products_revenue": _bar(
            chart_data["top_products_revenue"],
            x="Sales",
            y="Product",
            title="Top 10 produits par chiffre d'affaires",
            orientation="h",
        ),
        "top_products_quantity": _bar(
            chart_data["top_products_quantity"],
            x="Quantity Ordered",
            y="Product",
            title="Top 10 produits par quantité vendue",
            orientation="h",
        ),
        "sales_by_city": _bar(
            chart_data["sales_by_city"],
            x="Sales",
            y="City",
            title="Chiffre d'affaires par ville",
            orientation="h",
        ),
        "sales_by_hour": px.line(
            chart_data["sales_by_hour"],
            x="Hour",
            y="Sales",
            markers=True,
            title="Chiffre d'affaires par heure",
        ),
        "sales_by_day": px.bar(
            chart_data["sales_by_day"],
            x="Day",
            y="Sales",
            title="Chiffre d'affaires par jour",
        ),
        "sales_distribution": px.histogram(
            chart_data["sales_distribution"],
            x="Sales",
            nbins=50,
            title="Distribution des ventes",
        ),
    }


def _group_sum(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
    limit: int | None,
) -> pd.DataFrame:
    grouped = (
        df.groupby(group_column, dropna=False)[value_column]
        .sum()
        .reset_index()
        .sort_values(value_column, ascending=False)
    )
    return grouped.head(limit) if limit else grouped


def _bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    orientation: str = "v",
) -> object:
    import plotly.express as px

    fig = px.bar(df, x=x, y=y, title=title, orientation=orientation)
    if orientation == "h":
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig
