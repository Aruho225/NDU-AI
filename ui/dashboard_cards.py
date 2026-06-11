"""KPI stat cards for the dashboard."""

from __future__ import annotations

import html

import streamlit as st

from ui.dashboard_layout import section_panel


def _ring_card(label: str, value: str, pct: float, tip: str, color: str) -> str:
    pct_safe = max(0, min(100, pct))
    return f"""
    <div class="dash-stat-card">
      <div class="dash-stat-ring" style="--pct:{pct_safe}; --ring-color:{color};">
        <span>{pct_safe:.0f}%</span>
      </div>
      <div class="dash-stat-copy">
        <p class="dash-stat-label">{html.escape(label)}</p>
        <p class="dash-stat-value">{html.escape(value)}</p>
        <p class="dash-stat-tip-inline">{html.escape(tip)}</p>
      </div>
    </div>
    """


def render_stat_cards(summary: dict) -> None:
    total = summary["total"] or 1
    cards = [
        ("Total calls", str(summary["total"]), min(100, summary["total"] * 10), f"In {summary['inbound']} · Out {summary['outbound']}", "#00d4ff"),
        ("Successful", str(summary["successful"]), summary["success_rate"], f"{summary['success_rate']}% success rate", "#00e5c0"),
        ("Failed", str(summary["failed"]), summary["failed"] / total * 100, "Missed or failed calls", "#ff6b8a"),
        ("Outbound", str(summary["outbound"]), summary["outbound"] / total * 100, f"Avg {summary['avg_duration_sec']}s talk", "#3b82f6"),
        ("Talk time", f"{summary['total_talk_minutes']}m", min(100, summary["total_talk_minutes"] * 5), f"{summary['with_recording']} recordings", "#00d4ff"),
    ]
    with section_panel("Key metrics", "Summary cards — hover rings show relative share"):
        row = st.columns(5, gap="small")
        for col, (label, value, pct, tip, color) in zip(row, cards):
            with col:
                st.markdown(_ring_card(label, value, pct, tip, color), unsafe_allow_html=True)
