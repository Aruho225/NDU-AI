"""Quick Twilio voice setup check. Run: python twilio_check.py"""

from dotenv import load_dotenv

load_dotenv()

from ui.twilio_calls import get_webhook_base_url, twilio_config_issue


def main() -> None:
    issue = twilio_config_issue()
    base = get_webhook_base_url()
    print("Twilio voice check")
    print("-" * 40)
    if issue:
        print("BLOCKED:", issue)
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
