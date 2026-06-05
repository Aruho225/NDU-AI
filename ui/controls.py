import streamlit as st



from ui.auth import logout

from ui.controls_styles import SESSION_CONTROLS_CSS

from ui.ambient_layer import mic_label
from ui.theme import render_theme_toggle
from ui.voice_client import TTS_VOICES





def render_status_bar(session_live: bool, mute_mic: bool, username: str, tts_voice: str) -> None:

    status = "LIVE" if session_live else "PAUSED"

    mic = "MIC ON" if not mute_mic else "MUTED"

    status_class = "pill-live" if session_live else "pill-paused"

    st.markdown(

        f"""

        <div class="session-status-bar">

          <span class="pill {status_class}">● {status}</span>

          <span class="pill pill-voice">{mic}</span>

          <span class="pill pill-voice">{mic_label(f"Voice: {tts_voice}")}</span>

          <span class="pill pill-user">👤 {username}</span>

        </div>

        """,

        unsafe_allow_html=True,

    )





def render_session_controls() -> dict:

    st.markdown(SESSION_CONTROLS_CSS, unsafe_allow_html=True)



    with st.sidebar:

        with st.expander("Session settings", expanded=False):

            st.caption("Voice, cache & session options")

            if st.session_state.get("authenticated"):

                st.markdown(

                    f'<span class="session-user-chip">Signed in · {st.session_state.username}</span>',

                    unsafe_allow_html=True,

                )



            c1, c2 = st.columns(2)

            session_live = c1.toggle("Session live", value=True, key="ctrl_session_live")

            mute_mic = c2.toggle("Mute mic", value=False, key="ctrl_mute_mic")

            c3, c4 = st.columns(2)

            auto_play = c3.toggle("Auto-play", value=True, key="ctrl_auto_play")

            cache_enabled = c4.toggle("Cache", value=True, key="ctrl_cache")

            dark_mode = render_theme_toggle()

            tts_voice = st.selectbox("🎤 Voice", options=TTS_VOICES, index=0, key="ctrl_tts_voice")



            if st.session_state.get("authenticated"):

                if st.button("Sign out", use_container_width=True, key="ctrl_sign_out", type="primary"):

                    logout()

                    st.rerun()



    username = st.session_state.get("username") or "Guest"

    render_status_bar(session_live, mute_mic, username, tts_voice)



    return {

        "layout_mode": st.session_state.layout_mode,

        "session_live": session_live,

        "mute_mic": mute_mic,

        "auto_play": auto_play,

        "cache_enabled": cache_enabled,

        "tts_voice": tts_voice,

        "dark_mode": dark_mode,

    }


