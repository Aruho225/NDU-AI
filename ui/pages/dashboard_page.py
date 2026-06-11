import streamlit as st

from ui.app_state import refresh_call_history
from ui.call_analytics import daily_series, load_dashboard_calls, summarize_calls
from ui.call_notifications import refresh_notifications, render_notifications_panel
from ui.dashboard_cards import render_stat_cards
from ui.dashboard_charts import render_dashboard_charts
from ui.dashboard_filters import render_date_toolbar
from ui.dashboard_layout import render_page_header
from ui.dashboard_page_styles import DASHBOARD_PAGE_CSS
from ui.dashboard_report import render_reports_table


def render_dashboard_page() -> None:
    st.markdown(DASHBOARD_PAGE_CSS, unsafe_allow_html=True)
    st.markdown('<div class="dash-dark-scope">', unsafe_allow_html=True)

    refresh_call_history(sync_twilio=True)
    start, end = render_date_toolbar()
    if st.session_state.pop("_dash_force_refresh", False):
        refresh_call_history(sync_twilio=True)
        st.rerun()

    user_id = st.session_state.get("user_id")
    uid = int(user_id) if user_id is not None else None
    calls = load_dashboard_calls(uid, start, end)
    summary = summarize_calls(calls)
    series = daily_series(calls)
    refresh_notifications(calls)

    render_page_header(summary["total"], start.isoformat(), end.isoformat())
    render_stat_cards(summary)
    render_dashboard_charts(series, summary)

    tab_reports, tab_notify = st.tabs(["Reports", "Notifications"])
    with tab_reports:
        render_reports_table(calls)
    with tab_notify:
        render_notifications_panel()

    st.markdown("</div>", unsafe_allow_html=True)
