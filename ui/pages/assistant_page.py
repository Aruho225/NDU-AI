import html

import streamlit as st

from ui.assistants_config import assistant_runtime_status, get_assistant
from ui.layout_modes import CALLS, PHONE_NUMBERS, PLAYGROUND
from ui.twilio_calls import get_phone_number, get_webhook_base_url


def _page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="page-header"><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def _status_line(ok: bool, label: str) -> str:
    dot = "status-ok" if ok else "status-warn"
    text = "Connected" if ok else "Not configured"
    return f'<span class="status-dot {dot}"></span>{html.escape(label)}: {text}'


def render_assistant_page() -> None:
    assistant_id = st.session_state.get("selected_assistant_id", "ndu-main")
    assistant = get_assistant(assistant_id)
    status = assistant_runtime_status()
    phone = get_phone_number() or "—"
    webhook = get_webhook_base_url() or "—"

    _page_header(
        assistant["name"],
        assistant["description"],
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model", assistant["model"])
    c2.metric("Web voice", assistant["voice_web"])
    c3.metric("Phone voice", "Polly")
    c4.metric("Channels", len(assistant["channels"]))

    st.markdown('<div class="panel-card"><h3>Configuration</h3>', unsafe_allow_html=True)
    cols = st.columns(3)
    cols[0].markdown(
        f"""
        <div class="kv-item"><div class="k">Language model</div><div class="v">{html.escape(assistant["model"])}</div></div>
        """,
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        f"""
        <div class="kv-item"><div class="k">Web TTS voice</div><div class="v">{html.escape(assistant["voice_web"])}</div></div>
        """,
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        f"""
        <div class="kv-item"><div class="k">Phone STT</div><div class="v">{html.escape(assistant["stt_phone"])}</div></div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Assigned phone number</h3>', unsafe_allow_html=True)
    if status["phone_assigned"]:
        st.markdown(
            f'<div class="phone-card"><div class="number">{html.escape(phone)}</div>'
            f'<p class="list-row-meta">Inbound &amp; outbound voice · SMS enabled when webhook is running</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("No Twilio number assigned. Set `TWILIO_PHONE_NUMBER` in `.env`.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Channels &amp; topics</h3>', unsafe_allow_html=True)
    channels = "".join(f'<span class="channel-tag">{html.escape(c)}</span>' for c in assistant["channels"])
    tags = "".join(f'<span class="assistant-pill">{html.escape(t)}</span>' for t in assistant["tags"])
    st.markdown(f"{channels}<br><br>{tags}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Runtime status</h3>', unsafe_allow_html=True)
    st.markdown(
        "<br>".join(
            [
                _status_line(status["openai"], "OpenAI API"),
                _status_line(status["twilio"], "Twilio account"),
                _status_line(status["webhook"], "Voice webhook URL"),
                _status_line(status.get("livekit", False), "LiveKit"),
                _status_line(status.get("deepgram", False), "Deepgram realtime STT"),
                _status_line(status.get("voice_livekit", False), "LiveKit voice pipeline"),
            ]
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Quick actions")
    a1, a2, a3 = st.columns(3)
    if a1.button("Open playground", use_container_width=True, key="asst_go_play"):
        st.session_state.layout_mode = PLAYGROUND
        st.rerun()
    if a2.button("Phone numbers", use_container_width=True, key="asst_go_phone"):
        st.session_state.layout_mode = PHONE_NUMBERS
        st.rerun()
    if a3.button("View calls", use_container_width=True, key="asst_go_calls"):
        st.session_state.layout_mode = CALLS
        st.rerun()
