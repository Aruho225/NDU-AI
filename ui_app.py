import html

import streamlit as st
from dotenv import load_dotenv

from ui.app_state import init_state, submit_question
from ui.auth import render_login_gate
from ui.call_pages import render_call_detail_page, render_inbound_calls_page, render_outbound_calls_page
from ui.controls import render_session_controls
from ui.sidebar_chats import render_sidebar_chats
from ui.mobile_meta import inject_mobile_meta
from ui.presets import QUICK_PROMPTS
from ui.styles import APP_CSS
from ui.voice_client import transcribe_audio


def _to_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


load_dotenv()
st.set_page_config(
    page_title="NDU AI Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)
inject_mobile_meta()
st.markdown(APP_CSS, unsafe_allow_html=True)

init_state()
if not render_login_gate():
    st.stop()

controls = render_session_controls()
session_live = controls["session_live"]
mute_mic = controls["mute_mic"]
auto_play = controls["auto_play"]
cache_enabled = controls["cache_enabled"]
tts_voice = controls["tts_voice"]

with st.sidebar:
    render_sidebar_chats()


def run_query(question: str) -> None:
    cache_hit = submit_question(question, cache_enabled=cache_enabled, tts_voice=tts_voice)
    st.session_state.layout_mode = "Answer Page"
    if cache_hit:
        st.info("Response served from cache for faster delivery.")


if st.session_state.layout_mode == "Ask Page":
    st.markdown(
        '<div class="mobile-tip">'
        "<strong>On your phone:</strong> use HTTPS or your PC’s LAN IP "
        "(e.g. <code>http://192.168.x.x:8501</code>). "
        "Record voice below or upload a voice note (.m4a, .webm)."
        "</div>",
        unsafe_allow_html=True,
    )
    hit_rate = 0 if st.session_state.total_queries == 0 else int(
        (st.session_state.cache_hits / st.session_state.total_queries) * 100
    )
    status = "LIVE" if session_live else "PAUSED"
    mic = "MUTED" if mute_mic else "READY"
    wave_state = "wave-paused" if (not session_live or mute_mic) else "wave-live"
    bg_wave_state = "bg-wave bg-wave-paused" if (not session_live or mute_mic) else "bg-wave"
    st.markdown(
        """
        <div class="hero">
            <h1 class="brand"><span class="brand-accent">NDU</span> AI Assistant</h1>
            <p class="tagline">Modern interface for quick university support.</p>
            <span class="pill">Admissions</span><span class="pill">Fees Guidance</span>
            <span class="pill">Academic Support</span><span class="pill">ICT Help</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="bg-wave-layer" aria-hidden="true">
          <div class="{bg_wave_state}">
            <span></span><span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span><span></span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="console-bar">
          <span class="badge">{status}</span><span class="badge">{mic}</span>
          <span class="badge">Voice: {tts_voice}</span><span class="badge">Cache: {hit_rate}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="voice-wave-wrap">
          <div class="voice-wave {wave_state}">
            <span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span>
          </div>
          <span class="wave-label">Voice Activity</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    metrics = st.columns(3)
    metrics[0].metric("Latency", f"{st.session_state.last_latency_ms} ms")
    metrics[1].metric("Queries", st.session_state.total_queries)
    metrics[2].metric("Cache hits", st.session_state.cache_hits)
    st.caption("SQLite: `chat_history.db` · Adjust settings in the sidebar panel.")

    with st.form("assistant_form", clear_on_submit=True):
        prompt = st.text_area(
            "Command Center",
            placeholder="Example: How do I apply for the August intake?",
            height=100,
        )
        submitted = st.form_submit_button("Send", use_container_width=True)

    if submitted and session_live:
        run_query(prompt)
    elif submitted:
        st.warning("Session is paused. Turn on **Session live** in the sidebar.")

    st.subheader("Quick Actions")
    for idx, text in enumerate(QUICK_PROMPTS):
        if st.button(text, key=f"preset_{idx}", use_container_width=True):
            if session_live:
                run_query(text)
            else:
                st.warning("Session is paused.")

    st.subheader("Voice Input")
    mic_audio = st.audio_input("Record with microphone", key="mic_input")
    audio_file = st.file_uploader(
        "Or upload a voice note",
        type=["wav", "mp3", "m4a", "webm", "ogg"],
        help="On iPhone: use Voice Memos, then upload the .m4a file here.",
    )

    if st.button("Transcribe and Ask", use_container_width=True):
        if not session_live:
            st.warning("Session is paused. Resume in the sidebar.")
        elif mute_mic:
            st.warning("Microphone is muted in the sidebar.")
        else:
            source = mic_audio or audio_file
            if not source:
                st.warning("Record audio or upload a file first.")
            else:
                with st.spinner("Transcribing voice..."):
                    transcript, error = transcribe_audio(source.getvalue(), source.name)
                if error:
                    st.error(error)
                else:
                    run_query(transcript)
                    st.success("Voice message processed.")
elif st.session_state.layout_mode == "Answer Page":
    st.subheader("Answer Page")
    st.caption("Focused layout for selected chat only.")
    if st.button("Back To Ask Page", use_container_width=True):
        st.session_state.layout_mode = "Ask Page"
elif st.session_state.layout_mode == "Inbound Calls Page":
    render_inbound_calls_page()
elif st.session_state.layout_mode == "Outbound Calls Page":
    render_outbound_calls_page()
elif st.session_state.layout_mode == "Call Detail Page":
    render_call_detail_page()

if st.session_state.latest_audio:
    st.subheader("Assistant Voice Reply")
    st.audio(
        st.session_state.latest_audio,
        format="audio/mp3",
        autoplay=auto_play,
    )

if st.session_state.history and st.session_state.layout_mode in {"Ask Page", "Answer Page"}:
    selected = st.session_state.history[st.session_state.selected_chat_idx]
    if st.session_state.layout_mode == "Answer Page":
        st.markdown(
            f'<div class="user-bubble"><strong>You</strong><br>{_to_html(selected["q"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="assistant-bubble"><strong>NDU AI Assistant</strong><br>{_to_html(selected["a"])}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.subheader("Conversation")
        for item in st.session_state.history[:8]:
            st.markdown(
                f'<div class="user-bubble"><strong>You</strong><br>{_to_html(item["q"])}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="assistant-bubble"><strong>NDU AI Assistant</strong><br>{_to_html(item["a"])}</div>',
                unsafe_allow_html=True,
            )
            st.divider()
elif st.session_state.layout_mode == "Ask Page":
    st.markdown(
        '<div class="note">Start by asking anything about admissions, fees, programs, or portal support.</div>',
        unsafe_allow_html=True,
    )
