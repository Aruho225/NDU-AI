"""Organised chart sections for the dashboard."""

from __future__ import annotations

import streamlit as st

from ui.dashboard_layout import empty_state, section_panel
from ui.dashboard_plotly_bars import render_bar_chart, render_progress_bars
from ui.dashboard_plotly_donuts import render_donut_row
from ui.dashboard_plotly_lines import render_line_charts


def render_dashboard_charts(series: list[dict], summary: dict) -> None:
    if not series and not summary.get("total"):
        empty_state("No calls in this date range. Place or receive calls to populate the dashboard.")
        return

    with section_panel("Performance gauges", "Share of successful, inbound, outbound, and failed calls"):
        render_donut_row(summary)

    with section_panel("Trend analysis", "Call volume and outcomes over the selected period"):
        render_line_charts(series)

    left, right = st.columns([1.45, 1], gap="medium")
    with left:
        with section_panel("Daily breakdown", "Grouped bars by day"):
            render_bar_chart(series)
    with right:
        with section_panel("Performance bars", "Key ratios for the selected period"):
            render_progress_bars(summary)
