"""In-app notifications for call events."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from ui.call_analytics import classify_outcome, contact_number
from ui.dashboard_layout import section_panel


def _seen_ids() -> set[int]:
    raw = st.session_state.get("dash_seen_call_ids") or []
    return set(int(x) for x in raw)


def refresh_notifications(calls: list[dict[str, Any]]) -> list[dict[str, str]]:
    seen = _seen_ids()
    fresh: list[dict[str, str]] = []
    for call in calls[:40]:
        call_id = int(call.get("id") or 0)
        if not call_id or call_id in seen:
            continue
        direction = "Inbound" if call.get("direction") == "inbound" else "Outbound"
        outcome = classify_outcome(call.get("status", ""))
        level = "alert" if outcome == "failed" else "info"
        fresh.append(
            {
                "id": str(call_id),
                "level": level,
                "title": f"{direction} call — {call.get('status', 'unknown')}",
                "body": f"{contact_number(call)} · {(call.get('created_at') or '')[:16]}",
            }
        )
    stored = list(st.session_state.get("dash_notifications") or [])
    known = {row.get("id") for row in stored}
    for item in fresh:
        if item["id"] not in known:
            stored.insert(0, item)
            known.add(item["id"])
    st.session_state.dash_notifications = stored[:25]
    st.session_state.dash_seen_call_ids = list(seen | {int(c.get("id") or 0) for c in calls[:40]})
    return st.session_state.dash_notifications


def render_notifications_panel() -> None:
    items = list(st.session_state.get("dash_notifications") or [])
    with section_panel("Call notifications", "Recent inbound, outbound, and failed call events"):
        if not items:
            st.caption("New call activity will appear here.")
            return
        for item in items[:12]:
            css = "dash-notify-alert" if item.get("level") == "alert" else "dash-notify-info"
            st.markdown(
                f"""
                <div class="dash-notify {css}">
                  <strong>{html.escape(item.get('title', 'Call'))}</strong>
                  <span>{html.escape(item.get('body', ''))}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("Clear notifications", key="dash_clear_notify", use_container_width=True):
            st.session_state.dash_notifications = []
            st.rerun()
