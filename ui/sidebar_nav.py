import base64
import html
from pathlib import Path

import streamlit as st

from ui.assistants_config import ASSISTANT_ID, ASSISTANTS
from ui.auth import logout
from ui.layout_modes import (
    ASSISTANT,
    CALL_DETAIL,
    CALLS,
    CONVERSATION,
    PHONE_NUMBERS,
    PLAYGROUND,
    SETTINGS,
    normalize_mode,
)
from ui.sidebar_theme import inject_sidebar_theme

BADGE_PATH = Path(__file__).resolve().parent / "assets" / "ndu_badge.png"


def _badge_uri() -> str:
    encoded = base64.b64encode(BADGE_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


def _current_nav_mode() -> str:
    mode = normalize_mode(st.session_state.layout_mode)
    if mode == CALL_DETAIL:
        return normalize_mode(st.session_state.get("call_return_page", CALLS))
    return mode


def _nav_to(mode: str, **extra) -> None:
    current = _current_nav_mode()
    if current == mode and not extra:
        return
    st.session_state.layout_mode = mode
    for key, value in extra.items():
        st.session_state[key] = value
    if mode != CALL_DETAIL:
        st.session_state.selected_call_recording = None
    st.rerun()


def _nav_button(label: str, mode: str, key: str, badge: str = "") -> None:
    active = _current_nav_mode() == mode
    text = f"{label} ({badge})" if badge else label
    # Include active state in key so Streamlit recreates the widget with the correct type.
    btn_key = f"{key}_{'on' if active else 'off'}"
    if st.button(
        text,
        key=btn_key,
        use_container_width=True,
        type="primary" if active else "secondary",
    ):
        _nav_to(mode)


def _render_brand() -> None:
    st.markdown(
        f"""
        <div class="ndu-sidebar-brand">
          <img src="{_badge_uri()}" alt="NDU" />
          <div>
            <p class="title">NDU Console</p>
            <p class="subtitle">AI Operations</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_assistants_list() -> None:
    st.markdown('<p class="ndu-nav-section">Assistants</p>', unsafe_allow_html=True)
    selected = st.session_state.get("selected_assistant_id", ASSISTANT_ID)
    on_assistant_page = normalize_mode(st.session_state.layout_mode) == ASSISTANT
    for item in ASSISTANTS:
        active = selected == item["id"] and on_assistant_page
        prefix = "● " if active else ""
        btn_key = f"asst_pick_{item['id']}_{'on' if active else 'off'}"
        if st.button(
            f"{prefix}{item['name']}",
            key=btn_key,
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.selected_assistant_id = item["id"]
            _nav_to(ASSISTANT)


def _render_workspace_nav() -> None:
    st.markdown('<p class="ndu-nav-section">Workspace</p>', unsafe_allow_html=True)
    chat_count = len(st.session_state.get("history") or [])
    call_count = len(st.session_state.get("call_history") or [])

    _nav_button("Playground", PLAYGROUND, "nav_playground")
    _nav_button("Conversations", CONVERSATION, "nav_conversation", str(chat_count) if chat_count else "")
    _nav_button("Phone numbers", PHONE_NUMBERS, "nav_phones")
    _nav_button("Calls", CALLS, "nav_calls", str(call_count) if call_count else "")


def _render_footer() -> None:
    st.markdown('<p class="ndu-nav-section">Account</p>', unsafe_allow_html=True)
    _nav_button("Settings", SETTINGS, "nav_settings")
    user = st.session_state.get("username") or "Guest"
    st.markdown(
        f'<div class="ndu-sidebar-user">Signed in as <strong>{html.escape(user)}</strong></div>',
        unsafe_allow_html=True,
    )
    if st.button("Sign out", key="sb_signout", use_container_width=True, type="secondary"):
        logout()
        st.rerun()


def render_sidebar() -> None:
    """Fixed sidebar — navigation only, no page-specific panels."""
    inject_sidebar_theme()
    _render_brand()
    _render_assistants_list()
    _render_workspace_nav()
    st.divider()
    _render_footer()
