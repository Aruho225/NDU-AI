import streamlit as st
from time import perf_counter

from ui.assistant_client import ask_assistant, validate_message
from ui.database import delete_turn, init_db, load_recent_turns, rename_turn, save_turn
from ui.voice_client import text_to_speech_bytes


def init_state() -> None:
    init_db()
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("latest_audio", None)
    st.session_state.setdefault("response_cache", {})
    st.session_state.setdefault("audio_cache", {})
    st.session_state.setdefault("last_latency_ms", 0)
    st.session_state.setdefault("cache_hits", 0)
    st.session_state.setdefault("total_queries", 0)
    st.session_state.setdefault("selected_chat_idx", 0)
    st.session_state.setdefault("layout_mode", "Ask Page")
    if not st.session_state.history:
        st.session_state.history = load_recent_turns(limit=8)
    if st.session_state.history:
        st.session_state.selected_chat_idx = max(
            0, min(st.session_state.selected_chat_idx, len(st.session_state.history) - 1)
        )


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

    turn_id = save_turn(clean_q, answer)
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
        st.session_state.layout_mode = "Ask Page"
    return True, "Chat deleted."
