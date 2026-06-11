"""Bar and progress charts for the dashboard."""

from __future__ import annotations

import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui.dashboard_theme import DASH_BLUE, DASH_CYAN, DASH_FAIL, DASH_MUTED, DASH_OK, DASH_TEAL, PLOTLY_LAYOUT


def _grouped_bars(frame: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    specs = [
        ("inbound", "Inbound", DASH_CYAN),
        ("outbound", "Outbound", DASH_BLUE),
        ("successful", "Successful", DASH_OK),
        ("failed", "Failed", DASH_FAIL),
    ]
    for key, label, color in specs:
        if key not in frame.columns:
            continue
        fig.add_trace(
            go.Bar(
                x=frame.index,
                y=frame[key],
                name=label,
                marker=dict(color=color, line=dict(width=0), opacity=0.92),
            )
        )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        barmode="group",
        height=280,
        legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def _progress_bar(label: str, pct: float, color: str) -> str:
    width = max(0, min(100, pct))
    return f"""
    <div class="dash-progress">
      <div class="dash-progress-head">
        <span>{html.escape(label)}</span>
        <strong>{width:.0f}%</strong>
      </div>
      <div class="dash-progress-track">
        <div class="dash-progress-fill" style="width:{width:.1f}%; background: linear-gradient(90deg, {color}, {DASH_TEAL});"></div>
      </div>
    </div>
    """


def render_bar_chart(series: list[dict]) -> None:
    if not series:
        st.caption("No daily data yet.")
        return
    frame = pd.DataFrame(series)
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.set_index("date").fillna(0)
    st.plotly_chart(_grouped_bars(frame), use_container_width=True, config={"displayModeBar": False})


def render_progress_bars(summary: dict) -> None:
    total = summary["total"] or 1
    bars = [
        ("Answered successfully", summary["success_rate"], DASH_OK),
        ("Inbound traffic", summary["inbound"] / total * 100, DASH_CYAN),
        ("Outbound traffic", summary["outbound"] / total * 100, DASH_BLUE),
        ("Failed / missed", summary["failed"] / total * 100, DASH_FAIL),
    ]
    for label, pct, color in bars:
        st.markdown(_progress_bar(label, pct, color), unsafe_allow_html=True)
