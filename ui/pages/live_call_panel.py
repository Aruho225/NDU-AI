import html
from datetime import timedelta

import streamlit as st

from ui.app_state import refresh_call_history
from ui.call_store import get_call_by_sid, is_call_active, load_watchable_calls


def _to_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def _render_transcript_lines(conversation: list[dict]) -> None:
    if not conversation:
        st.caption("Waiting for speech… The agent logs each turn as the call progresses.")
        return
    for turn in conversation:
        role = turn.get("role", "caller")
        label = "Caller" if role == "caller" else "NDU AI Assistant"
        css = "user-bubble" if role == "caller" else "assistant-bubble"
        st.markdown(
            f'<div class="{css}"><strong>{label}</strong><br>{_to_html(turn.get("text", ""))}</div>',
            unsafe_allow_html=True,
        )


@st.fragment(run_every=timedelta(seconds=2))
def _live_transcript_fragment(call_sid: str) -> None:
    refresh_call_history(sync_twilio=True)
    row = get_call_by_sid(call_sid)
    if not row:
        st.warning("Call record not found.")
        return

    status = (row.get("status") or "unknown").lower()
    live = is_call_active(status)
    dot_class = "status-ok" if live else "status-off"
    st.markdown(
        f'<p><span class="status-dot {dot_class}"></span> '
        f'<strong>Status:</strong> {html.escape(status)} · '
        f'<strong>Mode:</strong> {html.escape(row.get("voice_mode") or "—")}</p>',
        unsafe_allow_html=True,
    )

    meta = st.columns(3)
    meta[0].caption(f"From: {row.get('from_number') or '—'}")
    meta[1].caption(f"To: {row.get('to_number') or '—'}")
    meta[2].caption(f"Room: {row.get('livekit_room') or '—'}")

    _render_transcript_lines(row.get("conversation_log") or [])

    if row.get("recording_url"):
        st.caption("Recording saved — open call detail to listen.")
    elif not live:
        st.caption("Fetching recording from Twilio…")

    if not live:
        st.info("Call ended. Transcript and recording are kept in call detail below.")


def render_live_call_panel() -> None:
    user_id = st.session_state.get("user_id")
    refresh_call_history(sync_twilio=True)
    watchable = load_watchable_calls(int(user_id) if user_id is not None else None)

    watch_sid = st.session_state.get("live_watch_call_sid") or ""
    if not watch_sid and watchable:
        watch_sid = watchable[0].get("call_sid", "")
        st.session_state.live_watch_call_sid = watch_sid

    st.markdown(
        """
        <div class="panel-card live-call-panel">
          <h3>Live call · realtime transcript</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns([2, 2, 1])
    options = {
        c["call_sid"]: f"{c.get('direction', '?')} · {c.get('status', '')} · {c.get('call_sid', '')[:10]}…"
        for c in watchable
    }
    if watch_sid and watch_sid not in options:
        row = get_call_by_sid(watch_sid)
        if row:
            options[watch_sid] = f"{row.get('direction')} · {row.get('status')} · (watching)"

    with col_a:
        if options:
            pick = st.selectbox(
                "Active call",
                options=list(options.keys()),
                format_func=lambda sid: options[sid],
                index=list(options.keys()).index(watch_sid) if watch_sid in options else 0,
                key="live_call_pick",
            )
            st.session_state.live_watch_call_sid = pick
        else:
            st.caption("No active calls right now.")
            st.session_state.live_watch_call_sid = watch_sid or ""

    with col_b:
        st.session_state.live_auto_refresh = st.toggle(
            "Auto-refresh transcript",
            value=st.session_state.get("live_auto_refresh", True),
            key="live_auto_refresh_toggle",
        )

    with col_c:
        if st.button("Refresh now", key="live_refresh_btn", use_container_width=True):
            refresh_call_history(sync_twilio=True)
            st.rerun()

    sid = st.session_state.get("live_watch_call_sid") or ""
    if not sid:
        st.markdown(
            '<div class="note">Place an outbound call or answer an inbound call to see live transcription here.</div>',
            unsafe_allow_html=True,
        )
        return

    if st.session_state.get("live_auto_refresh", True):
        _live_transcript_fragment(sid)
    else:
        row = get_call_by_sid(sid)
        if row:
            _render_transcript_lines(row.get("conversation_log") or [])
        else:
            st.caption("Select or start a call.")
