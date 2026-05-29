import base64
from pathlib import Path

import streamlit as st

from ui.app_state import (
    delete_selected_call,
    delete_selected_chat,
    refresh_call_history,
    rename_selected_chat,
    start_outbound_call,
)
from ui.sidebar_styles import SIDEBAR_CSS
from ui.twilio_calls import twilio_configured

BADGE_PATH = Path(__file__).resolve().parent / "assets" / "ndu_badge.png"

NAV_PAGES = {
    "Ask Page": "Chats",
    "Answer Page": "Chats",
    "Inbound Calls Page": "Inbound",
    "Outbound Calls Page": "Outbound",
    "Call Detail Page": None,
}


def _short(text: str, length: int = 38) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= length else f"{clean[:length].rstrip()}..."


def _badge_uri() -> str:
    encoded = base64.b64encode(BADGE_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


def _calls_for_direction(direction: str) -> list[dict]:
    return [
        item
        for item in (st.session_state.get("call_history") or [])
        if item.get("direction") == direction
    ]


def _call_label(item: dict) -> str:
    direction = item.get("direction", "unknown")
    icon = "↓" if direction == "inbound" else "↑"
    number = item.get("from_number") if direction == "inbound" else item.get("to_number")
    number = number or "Unknown"
    status = item.get("status", "unknown")
    return f"{icon} {_short(number, 22)} · {status}"


def _open_call_detail(call_id: int, return_page: str) -> None:
    for idx, item in enumerate(st.session_state.call_history):
        if item.get("id") == call_id:
            st.session_state.selected_call_idx = idx
            break
    st.session_state.call_return_page = return_page
    st.session_state.layout_mode = "Call Detail Page"
    st.session_state.selected_call_recording = None


def _render_nav_links() -> None:
    st.markdown('<p class="chat-manage-label">Navigate</p>', unsafe_allow_html=True)
    current = st.session_state.layout_mode
    active_nav = NAV_PAGES.get(current)

    chat_type = "primary" if active_nav == "Chats" else "secondary"
    inbound_type = "primary" if active_nav == "Inbound" else "secondary"
    outbound_type = "primary" if active_nav == "Outbound" else "secondary"

    if st.button("Chats", use_container_width=True, type=chat_type, key="nav_chats"):
        st.session_state.layout_mode = "Ask Page"
        st.rerun()
    if st.button("Inbound calls", use_container_width=True, type=inbound_type, key="nav_inbound"):
        st.session_state.layout_mode = "Inbound Calls Page"
        st.rerun()
    if st.button("Outbound calls", use_container_width=True, type=outbound_type, key="nav_outbound"):
        st.session_state.layout_mode = "Outbound Calls Page"
        st.rerun()


def _render_header(chat_count: int) -> None:
    st.markdown(
        f"""
        <div class="chats-header">
          <h3>Recent Chats</h3>
          <span class="chats-count">{chat_count}</span>
        </div>
        <div class="mobile-tip-box">☰ Tap the menu icon if the sidebar is hidden on your phone.</div>
        """,
        unsafe_allow_html=True,
    )


def _render_calls_header(title: str, call_count: int) -> None:
    st.markdown(
        f"""
        <div class="chats-header">
          <h3>{title}</h3>
          <span class="chats-count">{call_count}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_empty_state() -> None:
    st.markdown(
        f"""
        <div class="chats-empty">
          <img src="{_badge_uri()}" alt="NDU crest" />
          <strong>No chats yet</strong>
          <span>Ask a question on the main page to start your conversation history.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_calls_empty_state(message: str) -> None:
    st.markdown(
        f"""
        <div class="chats-empty">
          <strong>No calls yet</strong>
          <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_chats_section() -> None:
    history = st.session_state.history
    _render_header(len(history))

    if history:
        for idx, item in enumerate(history[:20]):
            active = (
                idx == st.session_state.selected_chat_idx
                and st.session_state.layout_mode in {"Ask Page", "Answer Page"}
            )
            label = ("● " if active else "") + _short(item["q"])
            if st.button(label, key=f"chat_pick_{idx}", use_container_width=True):
                st.session_state.selected_chat_idx = idx
                st.session_state.layout_mode = "Answer Page"
                st.rerun()

        st.markdown('<p class="chat-manage-label">Manage selected</p>', unsafe_allow_html=True)
        selected = history[st.session_state.selected_chat_idx]
        rename_value = st.text_input(
            "Rename selected question",
            value=selected["q"],
            key=f"rename_text_{st.session_state.selected_chat_idx}",
            label_visibility="collapsed",
        )
        r_col, d_col = st.columns(2)
        if r_col.button("Rename", use_container_width=True):
            ok, message = rename_selected_chat(rename_value)
            st.success(message) if ok else st.warning(message)
        if d_col.button("Delete", use_container_width=True):
            ok, message = delete_selected_chat()
            st.success(message) if ok else st.warning(message)
    else:
        _render_empty_state()


def _render_outbound_dial_panel() -> None:
    st.markdown('<p class="chat-manage-label">Quick dial</p>', unsafe_allow_html=True)
    if not twilio_configured():
        st.caption("Add Twilio credentials and TWILIO_WEBHOOK_BASE_URL in `.env`.")
    phone_number = st.text_input(
        "Phone number",
        placeholder="+256700000000",
        key="outbound_phone_sidebar",
        label_visibility="collapsed",
    )
    if st.button("Place outbound call", use_container_width=True, key="place_outbound_sidebar"):
        ok, message = start_outbound_call(phone_number)
        if ok:
            st.session_state.layout_mode = "Outbound Calls Page"
        st.success(message) if ok else st.warning(message)


def _render_call_sidebar_list(calls: list[dict], return_page: str, empty_message: str) -> None:
    if st.button("Refresh calls", use_container_width=True, key=f"refresh_{return_page}"):
        refresh_call_history()
        st.rerun()

    if not calls:
        _render_calls_empty_state(empty_message)
        return

    for idx, item in enumerate(calls[:20]):
        active = False
        if st.session_state.layout_mode == "Call Detail Page" and st.session_state.call_history:
            selected = st.session_state.call_history[st.session_state.selected_call_idx]
            active = item.get("id") == selected.get("id")
        label = ("● " if active else "") + _call_label(item)
        if st.button(label, key=f"call_pick_{return_page}_{item.get('id')}_{idx}", use_container_width=True):
            _open_call_detail(int(item["id"]), return_page)
            st.rerun()

    if st.button("Delete selected call", use_container_width=True, key=f"delete_call_{return_page}"):
        ok, message = delete_selected_call()
        st.success(message) if ok else st.warning(message)


def _render_inbound_sidebar() -> None:
    refresh_call_history()
    calls = _calls_for_direction("inbound")
    _render_calls_header("Inbound", len(calls))
    _render_call_sidebar_list(
        calls,
        "Inbound Calls Page",
        "Inbound calls to your Twilio number will appear here.",
    )


def _render_outbound_sidebar() -> None:
    refresh_call_history()
    calls = _calls_for_direction("outbound")
    _render_calls_header("Outbound", len(calls))
    _render_outbound_dial_panel()
    _render_call_sidebar_list(
        calls,
        "Outbound Calls Page",
        "Outbound calls you place will appear here.",
    )


def render_sidebar_chats() -> None:
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    _render_nav_links()

    layout = st.session_state.layout_mode
    if layout == "Inbound Calls Page":
        _render_inbound_sidebar()
    elif layout == "Outbound Calls Page":
        _render_outbound_sidebar()
    elif layout == "Call Detail Page":
        return_page = st.session_state.get("call_return_page", "Ask Page")
        if return_page == "Inbound Calls Page":
            _render_inbound_sidebar()
        elif return_page == "Outbound Calls Page":
            _render_outbound_sidebar()
        else:
            _render_chats_section()
    else:
        _render_chats_section()
