"""Date filter toolbar for the dashboard."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from ui.call_analytics import default_date_range, parse_dates


def render_date_toolbar() -> tuple[date, date]:
    default_start, default_end = default_date_range()
    st.session_state.setdefault("dash_start", default_start)
    st.session_state.setdefault("dash_end", default_end)

    st.markdown('<div class="dash-toolbar">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.2, 0.7])
    with c1:
        start = st.date_input("From date", value=st.session_state.dash_start, key="dash_date_start")
    with c2:
        end = st.date_input("To date", value=st.session_state.dash_end, key="dash_date_end")
    with c3:
        preset = st.selectbox(
            "Quick range",
            ["Custom", "Last 7 days", "Last 30 days", "Last 90 days"],
            key="dash_preset",
        )
    with c4:
        refresh = st.button("Refresh", use_container_width=True, key="dash_refresh_top")
    st.markdown("</div>", unsafe_allow_html=True)

    if preset == "Last 7 days":
        end = date.today()
        start = end - timedelta(days=6)
    elif preset == "Last 30 days":
        end = date.today()
        start = end - timedelta(days=29)
    elif preset == "Last 90 days":
        end = date.today()
        start = end - timedelta(days=89)

    start, end = parse_dates(start, end)
    st.session_state.dash_start = start
    st.session_state.dash_end = end
    if refresh:
        st.session_state["_dash_force_refresh"] = True
    return start, end
