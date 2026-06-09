import streamlit as st

from ui.auth import logout
from ui.voice_client import TTS_VOICES


def render_settings_page() -> None:
    st.markdown(
        """
        <div class="page-header">
          <h1>Settings</h1>
          <p>Session, voice, and cache options for the web playground.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="panel-card"><h3>Session</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.toggle("Session live", value=st.session_state.get("ctrl_session_live", True), key="ctrl_session_live")
    c2.toggle("Mute microphone", value=st.session_state.get("ctrl_mute_mic", False), key="ctrl_mute_mic")
    c3, c4 = st.columns(2)
    c3.toggle("Auto-play voice replies", value=st.session_state.get("ctrl_auto_play", True), key="ctrl_auto_play")
    c4.toggle("Response cache", value=st.session_state.get("ctrl_cache", True), key="ctrl_cache")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Voice</h3>', unsafe_allow_html=True)
    current_voice = st.session_state.get("ctrl_tts_voice", "alloy")
    voice_index = TTS_VOICES.index(current_voice) if current_voice in TTS_VOICES else 0
    st.selectbox("TTS voice (web)", options=TTS_VOICES, index=voice_index, key="ctrl_tts_voice")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Account</h3>', unsafe_allow_html=True)
    st.write(f"Signed in as **{st.session_state.get('username') or 'Guest'}**")
    if st.button("Sign out", type="primary", key="settings_signout"):
        logout()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Data is stored locally in `chat_history.db`.")
