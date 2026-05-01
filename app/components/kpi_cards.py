"""Composants de cartes KPI pour Streamlit."""

from __future__ import annotations

import streamlit as st


def render_kpi_cards(kpis: dict[str, object]) -> None:
    columns = st.columns(4)
    cards = [
        ("Chiffre d'affaires", f"${kpis.get('total_revenue', 0):,.2f}"),
        ("Commandes uniques", f"{kpis.get('unique_orders', 0):,}"),
        ("Unités vendues", f"{kpis.get('total_units_sold', 0):,}"),
        ("Panier moyen", f"${kpis.get('average_order_value', 0):,.2f}"),
    ]
    for column, (label, value) in zip(columns, cards):
        column.metric(label, value)

    columns = st.columns(4)
    secondary_cards = [
        ("Produit leader CA", _name_value(kpis.get("top_product_by_revenue", {}), money=True)),
        ("Produit leader volume", _name_value(kpis.get("top_product_by_quantity", {}), units=True)),
        ("Ville leader", _name_value(kpis.get("top_city_by_revenue", {}), money=True)),
        ("Meilleure heure", _name_value(kpis.get("best_sales_hour", {}), money=True)),
    ]
    for column, (label, value) in zip(columns, secondary_cards):
        column.metric(label, value)


def _name_value(item: object, money: bool = False, units: bool = False) -> str:
    if not isinstance(item, dict):
        return "N/A"
    name = item.get("name")
    value = item.get("value", 0)
    if money:
        return f"{name} | ${value:,.2f}"
    if units:
        return f"{name} | {value:,.0f}"
    return str(name)
