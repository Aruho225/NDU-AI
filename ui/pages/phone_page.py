import html
import os

import streamlit as st

from ui.telephony_config import telephony_status, use_livekit_voice, voice_mode
from ui.twilio_calls import get_account_sid, get_phone_number, get_webhook_base_url, twilio_configured
from ui.twilio_phone_setup import get_phone_webhook_status, sync_phone_webhooks


def _page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="page-header"><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def _mask_secret(value: str, show: int = 4) -> str:
    if len(value) <= show:
        return "••••"
    return value[:show] + "•" * (len(value) - show)


def _status_row(label: str, ok: bool) -> None:
    dot = "status-ok" if ok else "status-warn"
    text = "Ready" if ok else "Missing"
    st.markdown(
        f'<span class="status-dot {dot}"></span> {html.escape(label)}: <strong>{text}</strong>',
        unsafe_allow_html=True,
    )


def render_phone_page() -> None:
    _page_header(
        "Phone numbers",
        "Twilio numbers bridged to the NDU AI Assistant (LiveKit realtime or TwiML fallback).",
    )

    status = telephony_status()
    phone = get_phone_number()
    base = get_webhook_base_url()
    sid = get_account_sid()
    mode = voice_mode()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Voice mode", mode.upper())
    m2.metric("Pipeline", "Live" if status["voice_pipeline_ready"] else "Setup needed")
    m3.metric("Realtime STT", "Deepgram" if status["realtime_stt"] else "Twilio/Polly")
    m4.metric("Agent", str(status["agent_name"]))

    st.markdown('<div class="panel-card"><h3>System status</h3>', unsafe_allow_html=True)
    _status_row("Twilio credentials + phone number", bool(status["twilio"]))
    _status_row("Public webhook URL (ngrok)", bool(status["webhook_url"]))
    _status_row("LiveKit Cloud / server", bool(status["livekit"]))
    _status_row("Deepgram (realtime transcription)", bool(status["deepgram"]))
    _status_row("OpenAI", bool(status["openai"]))
    _status_row("Cartesia TTS", bool(status["cartesia"]))
    if use_livekit_voice():
        st.success("LiveKit voice pipeline is active. Run `python agent.py dev` alongside the webhook.")
    elif mode == "livekit":
        st.warning("VOICE_MODE=livekit but LiveKit env vars are incomplete. Calls fall back may fail.")
    else:
        st.info("VOICE_MODE=twiml — uses Twilio speech recognition and Polly (no LiveKit agent required).")
    st.markdown("</div>", unsafe_allow_html=True)

    if phone:
        st.markdown(
            f"""
            <div class="phone-card">
              <div class="list-row-meta">Primary · {html.escape(str(status["agent_name"]))}</div>
              <div class="number">{html.escape(phone)}</div>
              <div class="list-row-meta">Voice: {html.escape(mode)} · SMS enabled with webhook</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Set `TWILIO_PHONE_NUMBER` in `.env`.")

    webhook_status = get_phone_webhook_status()
    st.markdown('<div class="panel-card"><h3>Inbound phone webhook</h3>', unsafe_allow_html=True)
    if webhook_status.get("error"):
        st.warning(webhook_status["error"])
    elif webhook_status.get("ok"):
        st.success(f"Inbound calls to {webhook_status.get('phone')} route to this app.")
    else:
        current = webhook_status.get("current") or {}
        expected = webhook_status.get("expected") or {}
        st.error(
            "Inbound calls are misconfigured in Twilio. "
            "Outbound works because each call sets its own URL; inbound uses the phone number setting."
        )
        st.markdown(
            f"""
            - **Current voice URL:** `{current.get("voice_url") or "—"}`
            - **Should be:** `{expected.get("voice_url") or "—"}`
            """
        )
        if st.button("Fix inbound webhook now", type="primary", key="sync_twilio_phone"):
            result = sync_phone_webhooks(force=True)
            if result.get("ok"):
                st.success(result.get("message", "Updated."))
                st.rerun()
            else:
                st.error(result.get("message", "Update failed."))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Webhook endpoints</h3>', unsafe_allow_html=True)
    st.caption("Expose port **8000** and set `TWILIO_WEBHOOK_BASE_URL` to your HTTPS tunnel URL.")
    if base:
        st.code(
            f"""Health / status:  {base}/health
Telephony status:   {base}/telephony/status
Voice (inbound):    {base}/twilio/voice/inbound
Voice (outbound):   {base}/twilio/voice/outbound
SMS:                {base}/twilio/webhook""",
            language="text",
        )
        if st.button("Open telephony status JSON", key="open_tel_status"):
            st.markdown(f"[{base}/telephony/status]({base}/telephony/status)")
    else:
        st.warning("Set `TWILIO_WEBHOOK_BASE_URL` in `.env` (e.g. https://xxxx.ngrok-free.app).")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Start services</h3>', unsafe_allow_html=True)
    st.code(
        """# Terminal 1 — Twilio + SMS webhooks
python -m uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000

# Terminal 2 — LiveKit agent (required for VOICE_MODE=livekit)
python agent.py dev

# Terminal 3 — optional UI
python -m streamlit run ui_app.py

# Or use the helper script:
.\\scripts\\start_telephony.ps1""",
        language="powershell",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel-card"><h3>Twilio console setup</h3>', unsafe_allow_html=True)
    webhook = f"{base}/twilio/voice/inbound" if base else "https://YOUR-TUNNEL/twilio/voice/inbound"
    st.markdown(
        f"""
        1. **Phone number → Voice configuration** → *A call comes in* → **Webhook** → POST → `{webhook}`
        2. **Phone number → Messaging** → POST → `{base or "https://YOUR-TUNNEL"}/twilio/webhook`
        3. Set `.env`: `VOICE_MODE=livekit` for realtime Deepgram + Cartesia (recommended).
        4. Ensure `LIVEKIT_AGENT_NAME` matches the agent worker (`ndu-assistant` by default).
        5. Place a test call — check **Calls** in the console for live transcripts.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Credentials (masked)"):
        st.markdown(
            f"""
            <div class="kv-grid">
              <div class="kv-item"><div class="k">Account SID</div><div class="v">{html.escape(_mask_secret(sid) if sid else "—")}</div></div>
              <div class="kv-item"><div class="k">Auth token</div><div class="v">{"Set" if os.getenv("TWILIO_AUTH_TOKEN") else "—"}</div></div>
              <div class="kv-item"><div class="k">LiveKit URL</div><div class="v">{"Set" if os.getenv("LIVEKIT_URL") else "—"}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
