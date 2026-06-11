"""Quick Twilio voice setup check. Run: python twilio_check.py"""

from dotenv import load_dotenv

load_dotenv()

from ui.twilio_calls import get_webhook_base_url, twilio_configured


def main() -> None:
    base = get_webhook_base_url()
    print("Twilio voice check")
    print("-" * 40)
    if not twilio_configured():
        print("BLOCKED: Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env.")
    elif not base:
        print("BLOCKED: Set TWILIO_WEBHOOK_BASE_URL to your public ngrok URL (port 8000).")
    else:
        print("Credentials: OK")
    print("Webhook base:", base or "(not set)")
    if base:
        print("Inbound voice URL:", f"{base}/twilio/voice/inbound")
        print("Outbound voice URL:", f"{base}/twilio/voice/outbound")
        print("Health check URL:", f"{base}/health")
    print("-" * 40)
    print("Local server: uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000")
    print("Public tunnel: ngrok http 8000  (not Streamlit port 8501)")


if __name__ == "__main__":
    main()
