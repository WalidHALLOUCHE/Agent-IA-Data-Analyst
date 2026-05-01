"""Chart rendering helpers for Streamlit."""

from __future__ import annotations

import streamlit as st

from tools.sales_charts import build_sales_figures


def render_charts(chart_data: dict[str, object]) -> None:
    figures = build_sales_figures(chart_data)
    left, right = st.columns(2)
    with left:
        st.plotly_chart(figures["top_products_revenue"], use_container_width=True)
        st.plotly_chart(figures["sales_by_city"], use_container_width=True)
        st.plotly_chart(figures["sales_by_day"], use_container_width=True)
    with right:
        st.plotly_chart(figures["top_products_quantity"], use_container_width=True)
        st.plotly_chart(figures["sales_by_hour"], use_container_width=True)
        st.plotly_chart(figures["sales_distribution"], use_container_width=True)

