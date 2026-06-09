import streamlit as st

from ui.assistants_config import get_assistant
from ui.presets import QUICK_PROMPTS


def render_playground_page(
    *,
    session_live: bool,
    mute_mic: bool,
    on_submit,
    on_transcribe,
) -> None:
    assistant = get_assistant(st.session_state.get("selected_assistant_id", "ndu-main"))
    hit_rate = 0 if st.session_state.total_queries == 0 else int(
        (st.session_state.cache_hits / st.session_state.total_queries) * 100
    )
    status = "Live" if session_live else "Paused"
    mic = "Muted" if mute_mic else "Ready"

    st.markdown(
        f"""
        <div class="page-header">
          <h1>Playground</h1>
          <p>Test <strong>{assistant["name"]}</strong> before publishing to phone or SMS channels.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Session", status)
    m2.metric("Microphone", mic)
    m3.metric("Latency", f"{st.session_state.last_latency_ms} ms")
    m4.metric("Cache hit rate", f"{hit_rate}%")

    st.markdown('<div class="panel-card"><h3>Message</h3>', unsafe_allow_html=True)
    with st.form("playground_form", clear_on_submit=True):
        prompt = st.text_area(
            "Message",
            placeholder="Example: How do I apply for the August intake?",
            height=120,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send message", use_container_width=True)

    if submitted:
        if session_live:
            on_submit(prompt)
        else:
            st.warning("Session is paused. Enable **Session live** in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Quick prompts</h3>', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, text in enumerate(QUICK_PROMPTS):
        col = cols[idx % 2]
        if col.button(text, key=f"pg_preset_{idx}", use_container_width=True):
            if session_live:
                on_submit(text)
            else:
                st.warning("Session is paused.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Voice input</h3>', unsafe_allow_html=True)
    mic_audio = st.audio_input("Record", key="pg_mic")
    audio_file = st.file_uploader(
        "Upload voice note",
        type=["wav", "mp3", "m4a", "webm", "ogg"],
        label_visibility="collapsed",
    )
    if st.button("Transcribe and send", use_container_width=True, key="pg_transcribe"):
        if not session_live:
            st.warning("Session is paused.")
        elif mute_mic:
            st.warning("Microphone is muted.")
        else:
            source = mic_audio or audio_file
            if not source:
                st.warning("Record or upload audio first.")
            else:
                on_transcribe(source)
    st.markdown("</div>", unsafe_allow_html=True)
