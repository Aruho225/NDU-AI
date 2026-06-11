"""Donut / gauge charts for the dashboard."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from ui.dashboard_theme import (
    DASH_BLUE,
    DASH_CYAN,
    DASH_FAIL,
    DASH_MUTED,
    DASH_OK,
    DASH_PANEL_2,
    DASH_TEAL,
    PLOTLY_LAYOUT,
)


def _donut(pct: float, label: str, color: str, title: str) -> go.Figure:
    rest = max(0.0, 100.0 - pct)
    fig = go.Figure(
        data=[
            go.Pie(
                values=[pct, rest],
                labels=[label, ""],
                hole=0.72,
                marker=dict(colors=[color, DASH_PANEL_2], line=dict(color=DASH_PANEL_2, width=2)),
                textinfo="none",
                hoverinfo="skip",
                direction="clockwise",
                sort=False,
            )
        ]
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=title, x=0.5, font=dict(size=13, color=DASH_MUTED)),
        showlegend=False,
        height=190,
        annotations=[
            dict(
                text=f"<b>{pct:.0f}%</b>",
                x=0.5,
                y=0.5,
                font=dict(size=24, color=color),
                showarrow=False,
            )
        ],
    )
    return fig


def render_donut_row(summary: dict) -> None:
    total = summary["total"] or 1
    inbound_pct = summary["inbound"] / total * 100
    outbound_pct = summary["outbound"] / total * 100
    failed_pct = summary["failed"] / total * 100 if total else 0
    success_pct = summary["success_rate"]

    cols = st.columns(4, gap="small")
    charts = [
        (success_pct, "Success", DASH_OK, "Success rate"),
        (inbound_pct, "Inbound", DASH_CYAN, "Inbound share"),
        (outbound_pct, "Outbound", DASH_BLUE, "Outbound share"),
        (failed_pct, "Failed", DASH_FAIL, "Failed share"),
    ]
    for col, (pct, label, color, title) in zip(cols, charts):
        with col:
            st.plotly_chart(_donut(pct, label, color, title), use_container_width=True, config={"displayModeBar": False})
