"""Sync Twilio phone number webhooks from TWILIO_WEBHOOK_BASE_URL."""

from __future__ import annotations

from typing import Any

from ui.twilio_calls import get_phone_number, get_webhook_base_url, twilio_configured


def _expected_urls(base: str) -> dict[str, str]:
    return {
        "voice_url": f"{base}/twilio/voice/inbound",
        "status_callback": f"{base}/twilio/voice/status",
        "sms_url": f"{base}/twilio/webhook",
    }


def get_phone_webhook_status() -> dict[str, Any]:
    """Return current Twilio phone config vs expected URLs."""
    if not twilio_configured():
        return {"ok": False, "error": "Twilio is not configured."}

    base = get_webhook_base_url()
    if not base:
        return {"ok": False, "error": "TWILIO_WEBHOOK_BASE_URL is not set."}

    phone = get_phone_number()
    expected = _expected_urls(base)

    try:
        from twilio.rest import Client

        from ui.twilio_calls import get_account_sid, get_auth_token

        client = Client(get_account_sid(), get_auth_token())
        numbers = client.incoming_phone_numbers.list(phone_number=phone)
        if not numbers:
            return {"ok": False, "error": f"Twilio phone number {phone} not found in account."}

        row = numbers[0]
        current = {
            "voice_url": (row.voice_url or "").rstrip("/"),
            "voice_method": row.voice_method or "",
            "status_callback": (row.status_callback or "").rstrip("/"),
            "sms_url": (row.sms_url or "").rstrip("/"),
        }
        aligned = {
            "voice": current["voice_url"] == expected["voice_url"].rstrip("/"),
            "status": current["status_callback"] == expected["status_callback"].rstrip("/"),
            "sms": current["sms_url"] == expected["sms_url"].rstrip("/"),
        }
        return {
            "ok": all(aligned.values()),
            "phone": phone,
            "current": current,
            "expected": expected,
            "aligned": aligned,
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def sync_phone_webhooks(force: bool = False) -> dict[str, Any]:
    """
    Point the Twilio number's inbound voice + SMS webhooks at this app.
    Outbound calls already pass a per-call URL; inbound uses the number config.
    """
    status = get_phone_webhook_status()
    if status.get("error") and not status.get("current"):
        return {"ok": False, "message": status["error"], "updated": False}

    if status.get("ok") and not force:
        return {
            "ok": True,
            "message": "Twilio phone webhooks already match TWILIO_WEBHOOK_BASE_URL.",
            "updated": False,
            "phone": status.get("phone"),
        }

    base = get_webhook_base_url()
    expected = _expected_urls(base)
    phone = get_phone_number()

    try:
        from twilio.rest import Client

        from ui.twilio_calls import get_account_sid, get_auth_token

        client = Client(get_account_sid(), get_auth_token())
        numbers = client.incoming_phone_numbers.list(phone_number=phone)
        if not numbers:
            return {"ok": False, "message": f"Phone {phone} not found.", "updated": False}

        numbers[0].update(
            voice_url=expected["voice_url"],
            voice_method="POST",
            voice_fallback_url=expected["voice_url"],
            voice_fallback_method="POST",
            status_callback=expected["status_callback"],
            status_callback_method="POST",
            sms_url=expected["sms_url"],
            sms_method="POST",
            trunk_sid="",
        )
        return {
            "ok": True,
            "message": f"Inbound webhooks updated for {phone}.",
            "updated": True,
            "phone": phone,
            "expected": expected,
        }
    except Exception as exc:
        return {"ok": False, "message": f"Could not update Twilio phone: {exc}", "updated": False}
