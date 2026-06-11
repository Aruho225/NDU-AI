import streamlit as st
from time import perf_counter

from ui.assistant_client import ask_assistant, validate_message
from ui.call_store import delete_call, load_recent_calls
from ui.call_sync import sync_calls
from ui.database import delete_turn, init_db, load_recent_turns, rename_turn, save_turn
from ui.auth import restore_session_from_cookie
from ui.assistants_config import ASSISTANT_ID
from ui.layout_modes import CALLS, CONVERSATION, DEFAULT_MODE, PLAYGROUND, normalize_mode
from ui.twilio_calls import fetch_recording_bytes, place_outbound_call
from ui.voice_client import text_to_speech_bytes


def init_state() -> None:
    init_db()
    restore_session_from_cookie()
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("latest_audio", None)
    st.session_state.setdefault("response_cache", {})
    st.session_state.setdefault("audio_cache", {})
    st.session_state.setdefault("last_latency_ms", 0)
    st.session_state.setdefault("cache_hits", 0)
    st.session_state.setdefault("total_queries", 0)
    st.session_state.setdefault("selected_chat_idx", 0)
    st.session_state.setdefault("selected_assistant_id", ASSISTANT_ID)
    st.session_state.setdefault("calls_tab", "all")
    st.session_state.setdefault("call_history", [])
    st.session_state.setdefault("selected_call_idx", 0)
    st.session_state.setdefault("call_filter", "All")
    st.session_state.setdefault("selected_call_recording", None)
    st.session_state.setdefault("call_return_page", CALLS)
    st.session_state.setdefault("live_watch_call_sid", "")
    st.session_state.setdefault("live_auto_refresh", True)
    st.session_state.setdefault("calls_table_open_id", None)
    st.session_state.setdefault("dash_notifications", [])
    st.session_state.setdefault("dash_seen_call_ids", [])
    if "layout_mode" in st.session_state:
        st.session_state.layout_mode = normalize_mode(st.session_state.layout_mode)
        st.session_state.call_return_page = normalize_mode(st.session_state.call_return_page)
    else:
        st.session_state.setdefault("layout_mode", DEFAULT_MODE)
    user_id = st.session_state.get("user_id")
    if not st.session_state.history and user_id is not None:
        st.session_state.history = load_recent_turns(int(user_id), limit=8)
    if st.session_state.history:
        st.session_state.selected_chat_idx = max(
            0, min(st.session_state.selected_chat_idx, len(st.session_state.history) - 1)
        )
    refresh_call_history()


def refresh_call_history(sync_twilio: bool = True) -> None:
    user_id = st.session_state.get("user_id")
    uid = int(user_id) if user_id is not None else None
    current = load_recent_calls(uid, limit=30)
    if sync_twilio and current:
        sync_calls(current)
    st.session_state.call_history = load_recent_calls(uid, limit=30)
    if st.session_state.call_history:
        st.session_state.selected_call_idx = max(
            0,
            min(st.session_state.selected_call_idx, len(st.session_state.call_history) - 1),
        )
    else:
        st.session_state.selected_call_idx = 0


def start_outbound_call(phone_number: str) -> tuple[bool, str, str | None]:
    user_id = st.session_state.get("user_id")
    if user_id is None:
        return False, "You must be signed in to place outbound calls.", None
    ok, message, call_sid = place_outbound_call(phone_number, int(user_id))
    if ok:
        refresh_call_history()
        if call_sid:
            st.session_state.live_watch_call_sid = call_sid
            st.session_state.live_auto_refresh = True
            st.session_state.layout_mode = "Calls"
    return ok, message, call_sid


def load_selected_call_recording() -> tuple[bool, str]:
    calls = st.session_state.get("call_history") or []
    if not calls:
        st.session_state.selected_call_recording = None
        return False, "No call selected."

    idx = st.session_state.selected_call_idx
    selected = calls[idx]
    recording_url = selected.get("recording_url") or ""
    if not recording_url:
        st.session_state.selected_call_recording = None
        return False, "Recording not available yet. It may still be processing."

    audio, error = fetch_recording_bytes(recording_url)
    if error or not audio:
        st.session_state.selected_call_recording = None
        return False, error or "Could not load recording."
    st.session_state.selected_call_recording = audio
    return True, "Recording loaded."


def delete_selected_call() -> tuple[bool, str]:
    calls = st.session_state.get("call_history") or []
    if not calls:
        return False, "No call selected."

    idx = st.session_state.selected_call_idx
    selected = calls[idx]
    call_id = selected.get("id")
    if call_id is None:
        return False, "This call cannot be deleted."

    delete_call(int(call_id))
    refresh_call_history()
    st.session_state.selected_call_recording = None
    if not st.session_state.call_history:
        st.session_state.layout_mode = st.session_state.get("call_return_page", CALLS)
    return True, "Call removed from history."


def submit_question(question: str, cache_enabled: bool, tts_voice: str) -> bool:
    issue = validate_message(question)
    if issue:
        st.warning(issue)
        return False

    clean_q = question.strip()
    started = perf_counter()
    answer = st.session_state.response_cache.get(clean_q) if cache_enabled else None
    cache_hit = answer is not None
    if answer is None:
        with st.spinner("Getting response..."):
            answer = ask_assistant(clean_q)
        if cache_enabled:
            st.session_state.response_cache[clean_q] = answer
    else:
        st.session_state.cache_hits += 1

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.warning("You must be signed in to save chats.")
        return False
    turn_id = save_turn(clean_q, answer, int(user_id))
    st.session_state.history.insert(0, {"id": turn_id, "q": clean_q, "a": answer})
    st.session_state.selected_chat_idx = 0
    st.session_state.total_queries += 1
    audio_key = f"{tts_voice}:{answer}"
    audio = st.session_state.audio_cache.get(audio_key) if cache_enabled else None
    if audio is None:
        audio, error = text_to_speech_bytes(answer, voice=tts_voice)
        st.session_state.latest_audio = None if error else audio
        if cache_enabled and audio:
            st.session_state.audio_cache[audio_key] = audio
    else:
        st.session_state.latest_audio = audio
    st.session_state.last_latency_ms = int((perf_counter() - started) * 1000)
    return cache_hit


def rename_selected_chat(new_question: str) -> tuple[bool, str]:
    clean = new_question.strip()
    if not clean:
        return False, "Question title cannot be empty."
    if not st.session_state.history:
        return False, "No chat selected."

    idx = st.session_state.selected_chat_idx
    selected = st.session_state.history[idx]
    turn_id = selected.get("id")
    if turn_id is None:
        return False, "This chat cannot be renamed yet."

    rename_turn(int(turn_id), clean)
    st.session_state.history[idx]["q"] = clean
    return True, "Chat renamed."


def delete_selected_chat() -> tuple[bool, str]:
    if not st.session_state.history:
        return False, "No chat selected."

    idx = st.session_state.selected_chat_idx
    selected = st.session_state.history[idx]
    turn_id = selected.get("id")
    if turn_id is None:
        return False, "This chat cannot be deleted yet."

    delete_turn(int(turn_id))
    st.session_state.history.pop(idx)
    if st.session_state.history:
        st.session_state.selected_chat_idx = max(0, idx - 1)
    else:
        st.session_state.selected_chat_idx = 0
        st.session_state.layout_mode = PLAYGROUND
    return True, "Chat deleted."
