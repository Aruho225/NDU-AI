"""Section layout helpers for the dashboard."""

from __future__ import annotations

import html

import streamlit as st


def render_page_header(total: int, start: str, end: str) -> None:
    st.markdown(
        f"""
        <div class="dash-topbar">
          <div>
            <p class="dash-eyebrow">NDU Call Operations</p>
            <h1>Analytics Dashboard</h1>
            <p class="dash-sub">Period: {html.escape(start)} → {html.escape(end)}</p>
          </div>
          <div class="dash-total-pill">
            <span>Total calls</span>
            <strong>{total}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = "") -> None:
    sub = f'<p>{html.escape(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="dash-section-head">
          <h2>{html.escape(title)}</h2>
          {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_panel(title: str, subtitle: str = ""):
    section_header(title, subtitle)
    return st.container(border=True)


def empty_state(message: str) -> None:
    st.markdown(
        f'<div class="dash-empty">{html.escape(message)}</div>',
        unsafe_allow_html=True,
    )
