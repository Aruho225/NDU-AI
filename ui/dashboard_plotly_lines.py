"""Glowing line charts for the dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.dashboard_theme import DASH_CYAN, DASH_FAIL, DASH_MUTED, DASH_OK, PLOTLY_LAYOUT


def _glow_line(frame: pd.DataFrame, columns: list[tuple[str, str]], height: int = 300) -> go.Figure:
    fig = go.Figure()
    for col, color in columns:
        if col not in frame.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=frame.index,
                y=frame[col],
                mode="lines+markers",
                name=col.title(),
                line=dict(color=color, width=3, shape="spline"),
                marker=dict(size=6, color=color),
                fill="tozeroy" if col == "total" else None,
                fillcolor="rgba(0, 212, 255, 0.1)" if col == "total" else None,
            )
        )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=height,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0),
    )
    return fig


def render_line_charts(series: list[dict]) -> None:
    if not series:
        st.caption("No trend data yet.")
        return
    frame = pd.DataFrame(series)
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.set_index("date").fillna(0)
    frame["total"] = frame.get("inbound", 0) + frame.get("outbound", 0)

    left, right = st.columns(2)
    with left:
        st.markdown('<p class="dash-chart-label">Call volume</p>', unsafe_allow_html=True)
        st.plotly_chart(
            _glow_line(frame, [("total", DASH_CYAN)]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
    with right:
        st.markdown('<p class="dash-chart-label">Successful vs failed</p>', unsafe_allow_html=True)
        st.plotly_chart(
            _glow_line(frame, [("successful", DASH_OK), ("failed", DASH_FAIL)]),
            use_container_width=True,
            config={"displayModeBar": False},
        )
