import html

import streamlit as st

from ui.text_format import format_chat_html
from ui.app_state import (
    delete_selected_call,
    load_selected_call_recording,
    refresh_call_history,
    start_outbound_call,
)
from ui.twilio_calls import twilio_configured


def _to_html(text: str) -> str:
    return format_chat_html(text)


def _short_time(value: str) -> str:
    clean = (value or "").strip()
    if not clean:
        return "—"
    return clean.replace("T", " ")[:16]


def _short_label(text: str, length: int = 42) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= length else f"{clean[:length].rstrip()}..."


def _calls_for_direction(direction: str) -> list[dict]:
    return [
        item
        for item in (st.session_state.get("call_history") or [])
        if item.get("direction") == direction
    ]


def _open_call_detail(call_id: int, return_page: str) -> None:
    for idx, item in enumerate(st.session_state.call_history):
        if item.get("id") == call_id:
            st.session_state.selected_call_idx = idx
            break
    st.session_state.call_return_page = return_page
    st.session_state.layout_mode = "Call Detail Page"
    st.session_state.selected_call_recording = None


def _render_call_list(calls: list[dict], return_page: str, empty_message: str) -> None:
    if not calls:
        st.markdown(f'<div class="note">{html.escape(empty_message)}</div>', unsafe_allow_html=True)
        return

    for item in calls[:20]:
        number = item.get("from_number") if item.get("direction") == "inbound" else item.get("to_number")
        label = _short_label(f"{number or 'Unknown'} · {item.get('status', 'unknown')}")
        c1, c2 = st.columns([4, 1])
        with c1:
            if st.button(label, key=f"main_call_{return_page}_{item.get('id')}", use_container_width=True):
                _open_call_detail(int(item["id"]), return_page)
                st.rerun()
        with c2:
            st.caption(_short_time(item.get("created_at", "")))


def render_inbound_calls_page() -> None:
    refresh_call_history()
    calls = _calls_for_direction("inbound")

    st.subheader("Inbound Calls")
    st.caption("Calls received on your Twilio number. Select a call to hear the recording and read the transcript.")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total inbound", len(calls))
    completed = sum(1 for item in calls if item.get("status") == "completed")
    m2.metric("Completed", completed)
    m3.metric("With recording", sum(1 for item in calls if item.get("recording_url")))

    if st.button("Refresh inbound calls", use_container_width=True, key="refresh_inbound_main"):
        refresh_call_history()
        st.rerun()

    _render_call_list(
        calls,
        "Inbound Calls Page",
        "No inbound calls yet. When someone calls your Twilio number, they will appear here.",
    )


def render_outbound_calls_page() -> None:
    refresh_call_history()
    calls = _calls_for_direction("outbound")

    st.subheader("Outbound Calls")
    st.caption("Place a call to a student or applicant, then review recordings and transcripts here.")

    st.markdown("#### Place outbound call")
    if not twilio_configured():
        st.info("Add Twilio credentials and TWILIO_WEBHOOK_BASE_URL in `.env` to enable outbound calling.")

    phone_number = st.text_input(
        "Phone number",
        placeholder="+256700000000",
        key="outbound_phone_main",
    )
    if st.button("Place outbound call", use_container_width=True, key="place_outbound_main"):
        ok, message = start_outbound_call(phone_number)
        if ok:
            st.success(message)
            st.rerun()
        st.warning(message)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total outbound", len(calls))
    m2.metric("Completed", sum(1 for item in calls if item.get("status") == "completed"))
    m3.metric("With recording", sum(1 for item in calls if item.get("recording_url")))

    if st.button("Refresh outbound calls", use_container_width=True, key="refresh_outbound_main"):
        refresh_call_history()
        st.rerun()

    st.markdown("#### Outbound history")
    _render_call_list(
        calls,
        "Outbound Calls Page",
        "No outbound calls yet. Use the form above to place your first call.",
    )


def render_call_detail_page() -> None:
    calls = st.session_state.get("call_history") or []
    if not calls:
        st.warning("No call selected.")
        if st.button("Back", use_container_width=True, key="call_detail_back_empty"):
            st.session_state.layout_mode = st.session_state.get("call_return_page", "Ask Page")
        return

    selected_call = calls[st.session_state.selected_call_idx]
    direction = selected_call.get("direction", "unknown").title()
    return_page = st.session_state.get("call_return_page", "Ask Page")

    st.subheader("Call Detail")
    st.caption("Recording and conversation transcript for the selected call.")

    if st.button("Back", use_container_width=True, key="call_detail_back"):
        st.session_state.layout_mode = return_page
        st.session_state.selected_call_recording = None
        st.rerun()

    meta = st.columns(4)
    meta[0].metric("Direction", direction)
    meta[1].metric("Status", selected_call.get("status", "unknown"))
    meta[2].metric("Duration", f"{selected_call.get('duration_seconds', 0)} s")
    meta[3].metric("When", _short_time(selected_call.get("created_at", "")))

    st.markdown(
        f"""
        <div class="console-bar">
          <span class="badge">From: {html.escape(selected_call.get("from_number") or "—")}</span>
          <span class="badge">To: {html.escape(selected_call.get("to_number") or "—")}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.selected_call_recording is None:
        with st.spinner("Loading call recording..."):
            ok, message = load_selected_call_recording()
        if not ok:
            st.info(message)

    if st.session_state.selected_call_recording:
        st.subheader("Call Recording")
        st.audio(st.session_state.selected_call_recording, format="audio/mp3")

    st.subheader("Call Conversation")
    conversation = selected_call.get("conversation_log") or []
    if conversation:
        for turn in conversation:
            role = turn.get("role", "caller")
            label = "Caller" if role == "caller" else "NDU AI Assistant"
            css_class = "user-bubble" if role == "caller" else "assistant-bubble"
            st.markdown(
                f'<div class="{css_class}"><strong>{label}</strong><br>{_to_html(turn.get("text", ""))}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="note">No live conversation turns were captured for this call yet.</div>',
            unsafe_allow_html=True,
        )

    transcription = (selected_call.get("transcription") or "").strip()
    if transcription:
        st.subheader("Full Recording Transcription")
        st.markdown(
            f'<div class="assistant-bubble"><strong>Whisper transcript</strong><br>{_to_html(transcription)}</div>',
            unsafe_allow_html=True,
        )

    if st.button("Delete this call", use_container_width=True, key="call_detail_delete"):
        ok, message = delete_selected_call()
        if ok:
            st.session_state.layout_mode = return_page
            st.success(message)
            st.rerun()
        st.warning(message)
