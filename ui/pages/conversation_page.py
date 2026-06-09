import html

import streamlit as st

from ui.app_state import delete_selected_chat, rename_selected_chat
from ui.layout_modes import PLAYGROUND


def _to_html(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")


def _short(text: str, length: int = 48) -> str:
    clean = " ".join(text.split())
    return clean if len(clean) <= length else f"{clean[:length].rstrip()}..."


def render_conversation_page() -> None:
    history = st.session_state.get("history") or []

    st.markdown(
        """
        <div class="page-header">
          <h1>Conversations</h1>
          <p>Thread history from the playground. Select a thread to read the full exchange.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not history:
        st.markdown(
            '<div class="note">No conversations yet. Send a message from the Playground.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Go to Playground", use_container_width=True, key="conv_go_play"):
            st.session_state.layout_mode = PLAYGROUND
            st.rerun()
        return

    if st.session_state.selected_chat_idx >= len(history):
        st.session_state.selected_chat_idx = 0

    list_col, detail_col = st.columns([1, 2], gap="medium")

    with list_col:
        st.markdown('<div class="panel-card"><h3>Threads</h3>', unsafe_allow_html=True)
        for idx, item in enumerate(history[:30]):
            active = idx == st.session_state.selected_chat_idx
            label = ("● " if active else "") + _short(item["q"])
            if st.button(
                label,
                key=f"conv_thread_{idx}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                st.session_state.selected_chat_idx = idx
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with detail_col:
        selected = history[st.session_state.selected_chat_idx]
        st.markdown(
            f'<div class="panel-card"><h3>Thread detail</h3>'
            f'<p class="list-row-meta">#{selected.get("id", "—")} · {len(history)} saved</p></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="user-bubble"><strong>User</strong><br>{_to_html(selected["q"])}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="assistant-bubble"><strong>NDU AI Assistant</strong><br>{_to_html(selected["a"])}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state.latest_audio:
            st.subheader("Voice reply")
            st.audio(st.session_state.latest_audio, format="audio/mp3")

        st.markdown('<div class="panel-card"><h3>Manage thread</h3>', unsafe_allow_html=True)
        rename_value = st.text_input(
            "Rename thread",
            value=selected["q"],
            key="conv_rename",
        )
        c1, c2 = st.columns(2)
        if c1.button("Save title", key="conv_save", use_container_width=True):
            ok, msg = rename_selected_chat(rename_value)
            st.success(msg) if ok else st.warning(msg)
            if ok:
                st.rerun()
        if c2.button("Delete thread", key="conv_delete", use_container_width=True):
            ok, msg = delete_selected_chat()
            st.success(msg) if ok else st.warning(msg)
            if ok:
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
