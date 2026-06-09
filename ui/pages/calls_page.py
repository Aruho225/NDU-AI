import pandas as pd
import streamlit as st

from ui.app_state import refresh_call_history, start_outbound_call
from ui.call_pages import render_call_detail_page
from ui.layout_modes import CALL_DETAIL, CALLS
from ui.pages.live_call_panel import render_live_call_panel
from ui.twilio_calls import twilio_configured


def _short_time(value: str) -> str:
    clean = (value or "").strip()
    return "—" if not clean else clean.replace("T", " ")[:16]


def _open_call_detail(call_id: int) -> None:
    for idx, item in enumerate(st.session_state.call_history):
        if item.get("id") == call_id:
            st.session_state.selected_call_idx = idx
            break
    st.session_state.call_return_page = CALLS
    st.session_state.layout_mode = CALL_DETAIL
    st.session_state.selected_call_recording = None
    st.session_state.calls_table_open_id = call_id
    st.rerun()


def _render_outbound_dial() -> None:
    st.markdown('<div class="panel-card"><h3>Place outbound call</h3>', unsafe_allow_html=True)
    if not twilio_configured():
        st.warning("Add Twilio credentials and `TWILIO_WEBHOOK_BASE_URL` in `.env` to dial out.")
    else:
        st.caption("Uses your Twilio number. Live transcript appears below while the call is active.")

    phone_number = st.text_input(
        "Destination number (E.164)",
        placeholder="+256700000000",
        key="calls_outbound_phone",
    )
    if st.button("Start outbound call", type="primary", use_container_width=True, key="calls_place_outbound"):
        ok, message, call_sid = start_outbound_call(phone_number)
        if ok:
            st.success(message)
            if call_sid:
                st.session_state.live_watch_call_sid = call_sid
            st.rerun()
        else:
            st.warning(message)
    st.markdown("</div>", unsafe_allow_html=True)


def _build_calls_table(calls: list[dict]) -> tuple[pd.DataFrame, list[int]]:
    rows: list[dict] = []
    call_ids: list[int] = []
    for item in calls:
        direction = item.get("direction", "")
        contact = item.get("from_number") if direction == "inbound" else item.get("to_number")
        log = item.get("conversation_log") or []
        rows.append(
            {
                "Direction": "Inbound" if direction == "inbound" else "Outbound",
                "Contact": contact or "—",
                "Status": item.get("status", "—"),
                "Duration (s)": item.get("duration_seconds", 0),
                "Recording": "Yes" if item.get("recording_url") else "No",
                "Transcript": "Yes" if log else "No",
                "When": _short_time(item.get("created_at", "")),
            }
        )
        call_ids.append(int(item["id"]))
    return pd.DataFrame(rows), call_ids


def _render_calls_table(calls: list[dict]) -> None:
    st.markdown('<div class="panel-card"><h3>Call history</h3>', unsafe_allow_html=True)
    st.caption("Click a row to open transcript and recording.")

    if not calls:
        st.caption("No calls in this view yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    df, call_ids = _build_calls_table(calls)
    event = st.dataframe(
        df,
        key="calls_table",
        on_select="rerun",
        selection_mode="single-row",
        hide_index=True,
        use_container_width=True,
    )

    selected_rows: list[int] = []
    if event is not None and getattr(event, "selection", None):
        selected_rows = list(getattr(event.selection, "rows", None) or [])

    if selected_rows:
        row_idx = selected_rows[0]
        if 0 <= row_idx < len(call_ids):
            call_id = call_ids[row_idx]
            if st.session_state.get("calls_table_open_id") != call_id:
                _open_call_detail(call_id)
    else:
        st.caption("Select a row in the table to view transcript and recording.")

    st.markdown("</div>", unsafe_allow_html=True)


def render_calls_page() -> None:
    if st.session_state.layout_mode == CALL_DETAIL:
        render_call_detail_page()
        return

    refresh_call_history(sync_twilio=True)
    all_calls = st.session_state.get("call_history") or []

    st.markdown(
        """
        <div class="page-header">
          <h1>Calls</h1>
          <p>Outbound dialing, live transcripts during active calls, and call history.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_outbound_dial()
    render_live_call_panel()

    tab = st.radio(
        "Filter",
        ["All", "Inbound", "Outbound"],
        horizontal=True,
        key="calls_tab_radio",
        label_visibility="collapsed",
    )
    tab_key = tab.lower()
    st.session_state.calls_tab = tab_key

    if tab_key == "inbound":
        calls = [c for c in all_calls if c.get("direction") == "inbound"]
    elif tab_key == "outbound":
        calls = [c for c in all_calls if c.get("direction") == "outbound"]
    else:
        calls = all_calls

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Shown", len(calls))
    c2.metric("Completed", sum(1 for x in calls if x.get("status") == "completed"))
    c3.metric("With recording", sum(1 for x in calls if x.get("recording_url")))
    c4.metric("Total stored", len(all_calls))

    if st.button("Refresh call log", use_container_width=True, key="calls_refresh_main"):
        refresh_call_history(sync_twilio=True)
        st.rerun()

    _render_calls_table(calls)
