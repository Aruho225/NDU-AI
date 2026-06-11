import streamlit as st
from dotenv import load_dotenv

from ui.app_state import init_state, submit_question
from ui.auth import render_login_gate
from ui.controls import get_session_settings, init_control_defaults, render_top_status_bar
from ui.dashboard_styles import DASHBOARD_CSS
from ui.layout_modes import (
    ASSISTANT,
    CALL_DETAIL,
    CALLS,
    CONVERSATION,
    DASHBOARD,
    PHONE_NUMBERS,
    PLAYGROUND,
    SETTINGS,
    normalize_mode,
)
from ui.mobile_meta import inject_mobile_meta
from ui.pages.assistant_page import render_assistant_page
from ui.pages.calls_page import render_calls_page
from ui.pages.dashboard_page import render_dashboard_page
from ui.pages.conversation_page import render_conversation_page
from ui.pages.phone_page import render_phone_page
from ui.pages.playground_page import render_playground_page
from ui.pages.settings_page import render_settings_page
from ui.sidebar_nav import render_sidebar
from ui.styles import APP_CSS
from ui.voice_client import transcribe_audio


load_dotenv(override=True)
st.set_page_config(
    page_title="NDU Console",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_mobile_meta()
st.markdown(APP_CSS + DASHBOARD_CSS, unsafe_allow_html=True)

init_state()
init_control_defaults()
if not render_login_gate():
    st.stop()

settings = get_session_settings()
session_live = settings["session_live"]
mute_mic = settings["mute_mic"]
auto_play = settings["auto_play"]
cache_enabled = settings["cache_enabled"]
tts_voice = settings["tts_voice"]

with st.sidebar:
    render_sidebar()

mode = normalize_mode(st.session_state.layout_mode)
username = st.session_state.get("username") or "Guest"

if mode != SETTINGS:
    render_top_status_bar(session_live, mute_mic, username, tts_voice)


def run_query(question: str) -> None:
    cache_hit = submit_question(question, cache_enabled=cache_enabled, tts_voice=tts_voice)
    st.session_state.layout_mode = CONVERSATION
    if cache_hit:
        st.info("Response served from cache.")


def handle_transcribe(source) -> None:
    with st.spinner("Transcribing..."):
        transcript, error = transcribe_audio(source.getvalue(), source.name)
    if error:
        st.error(error)
    else:
        run_query(transcript)
        st.success("Voice message sent.")


if mode == ASSISTANT:
    render_assistant_page()
elif mode == DASHBOARD:
    render_dashboard_page()
elif mode == PLAYGROUND:
    render_playground_page(
        session_live=session_live,
        mute_mic=mute_mic,
        on_submit=run_query,
        on_transcribe=handle_transcribe,
    )
    if st.session_state.history and st.session_state.layout_mode == PLAYGROUND:
        with st.expander("Latest replies", expanded=False):
            for item in st.session_state.history[:4]:
                st.markdown(f"**Q:** {item['q']}")
                st.markdown(item["a"][:400] + ("…" if len(item["a"]) > 400 else ""))
                st.divider()
elif mode == CONVERSATION:
    render_conversation_page()
    if st.session_state.latest_audio:
        st.audio(st.session_state.latest_audio, format="audio/mp3", autoplay=auto_play)
elif mode == PHONE_NUMBERS:
    render_phone_page()
elif mode in {CALLS, CALL_DETAIL}:
    render_calls_page()
elif mode == SETTINGS:
    render_settings_page()
else:
    render_assistant_page()
