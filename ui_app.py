import html

import streamlit as st
from dotenv import load_dotenv

from ui.app_state import delete_selected_chat, init_state, rename_selected_chat, submit_question
from ui.presets import QUICK_PROMPTS
from ui.styles import APP_CSS
from ui.voice_client import TTS_VOICES, transcribe_audio


def _short(text: str, length: int = 38) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= length else f"{clean[:length].rstrip()}..."


def _to_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


load_dotenv()
st.set_page_config(page_title="NDU AI Assistant", page_icon="🎓", layout="centered")
st.markdown(APP_CSS, unsafe_allow_html=True)

init_state()
with st.sidebar:
    st.subheader("Console Controls")
    st.session_state.layout_mode = st.radio(
        "Page Layout",
        ["Ask Page", "Answer Page"],
        index=0 if st.session_state.layout_mode == "Ask Page" else 1,
    )
    session_live = st.toggle("Session live", value=True)
    mute_mic = st.toggle("Mute microphone", value=False)
    auto_play = st.toggle("Auto-play voice reply", value=True)
    cache_enabled = st.toggle("Cache responses", value=True)
    tts_voice = st.selectbox("Voice", options=TTS_VOICES, index=0)
    st.caption("Inspired by real-time voice console workflows.")
    st.divider()
    st.subheader("Recent Chats")
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history[:20]):
            active = idx == st.session_state.selected_chat_idx
            label = ("● " if active else "") + _short(item["q"])
            if st.button(label, key=f"chat_pick_{idx}", use_container_width=True):
                st.session_state.selected_chat_idx = idx
                st.session_state.layout_mode = "Answer Page"

        st.caption("Manage selected chat")
        selected = st.session_state.history[st.session_state.selected_chat_idx]
        rename_value = st.text_input(
            "Rename selected question",
            value=selected["q"],
            key=f"rename_text_{st.session_state.selected_chat_idx}",
        )
        r_col, d_col = st.columns(2)
        if r_col.button("Rename", use_container_width=True):
            ok, message = rename_selected_chat(rename_value)
            st.success(message) if ok else st.warning(message)
        if d_col.button("Delete", use_container_width=True):
            ok, message = delete_selected_chat()
            st.success(message) if ok else st.warning(message)
    else:
        st.caption("No chats yet. Start a conversation.")

def run_query(question: str) -> None:
    cache_hit = submit_question(question, cache_enabled=cache_enabled, tts_voice=tts_voice)
    st.session_state.layout_mode = "Answer Page"
    if cache_hit:
        st.info("Response served from cache for faster delivery.")


if st.session_state.layout_mode == "Ask Page":
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
            <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
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
    st.caption("Database: SQLite connected (`chat_history.db`) for persistent conversations.")

    with st.form("assistant_form", clear_on_submit=True):
        prompt = st.text_area(
            "Command Center",
            placeholder="Example: How do I apply for the August intake?",
            height=120,
        )
        submitted = st.form_submit_button("Send")

    if submitted and session_live:
        run_query(prompt)
    elif submitted:
        st.warning("Session is paused. Turn on 'Session live' to send messages.")

    st.subheader("Quick Actions")
    cols = st.columns(2)
    for idx, text in enumerate(QUICK_PROMPTS):
        if cols[idx % 2].button(text, key=f"preset_{idx}", use_container_width=True):
            if session_live:
                run_query(text)
            else:
                st.warning("Session is paused.")

    st.subheader("Voice Input")
    mic_audio = st.audio_input("Record with microphone")
    audio_file = st.file_uploader(
        "Or upload a voice note",
        type=["wav", "mp3", "m4a", "webm", "ogg"],
        help="Record from phone/PC and upload, then transcribe and ask.",
    )

    if st.button("Transcribe and Ask", use_container_width=True):
        if not session_live:
            st.warning("Session is paused. Resume to process voice.")
        elif mute_mic:
            st.warning("Microphone is muted in controls.")
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
else:
    st.subheader("Answer Page")
    st.caption("Focused layout for selected chat only.")
    if st.button("Back To Ask Page", use_container_width=False):
        st.session_state.layout_mode = "Ask Page"

if st.session_state.latest_audio:
    st.subheader("Assistant Voice Reply")
    st.audio(st.session_state.latest_audio, format="audio/mp3", autoplay=auto_play)

if st.session_state.history:
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
else:
    st.markdown('<div class="note">Start by asking anything about admissions, fees guidance, programs, or portal support.</div>', unsafe_allow_html=True)

