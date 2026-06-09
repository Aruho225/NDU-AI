import streamlit as st

from ui.controls_styles import SESSION_CONTROLS_CSS


def get_session_settings() -> dict:
    """Read playground session options (managed in Settings)."""
    return {
        "session_live": st.session_state.get("ctrl_session_live", True),
        "mute_mic": st.session_state.get("ctrl_mute_mic", False),
        "auto_play": st.session_state.get("ctrl_auto_play", True),
        "cache_enabled": st.session_state.get("ctrl_cache", True),
        "tts_voice": st.session_state.get("ctrl_tts_voice", "alloy"),
    }


def render_top_status_bar(session_live: bool, mute_mic: bool, username: str, tts_voice: str) -> None:
    status = "LIVE" if session_live else "PAUSED"
    mic = "MIC ON" if not mute_mic else "MUTED"
    status_class = "pill-live" if session_live else "pill-paused"
    st.markdown(SESSION_CONTROLS_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="session-status-bar">
          <span class="pill {status_class}">● {status}</span>
          <span class="pill pill-voice">{mic}</span>
          <span class="pill pill-voice">🎙 {tts_voice}</span>
          <span class="pill pill-user">👤 {username}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_control_defaults() -> None:
    st.session_state.setdefault("ctrl_session_live", True)
    st.session_state.setdefault("ctrl_mute_mic", False)
    st.session_state.setdefault("ctrl_auto_play", True)
    st.session_state.setdefault("ctrl_cache", True)
    st.session_state.setdefault("ctrl_tts_voice", "alloy")
