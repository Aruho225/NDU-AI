# NDU AI Assistant

AI operations console for **Ndejje University** — web chat, voice calls (inbound & outbound), live transcripts, and SMS via Twilio, with realtime voice powered by LiveKit.

| Component | Port | Purpose |
|-----------|------|---------|
| Streamlit UI | `8501` | Admin console, playground, calls, settings |
| FastAPI webhook | `8000` | Twilio voice/SMS webhooks |
| LiveKit agent | — | Realtime STT → LLM → TTS on phone calls |
| ngrok | `4040` (dashboard) | Public HTTPS tunnel to port 8000 |

---

## Features

- **Web console** — assistant dashboard, playground chat, conversations, call history
- **Inbound calls** — callers dial your Twilio number; AI answers via LiveKit
- **Outbound calls** — place calls from the Calls page
- **Live transcripts** — realtime turn logging during active calls
- **SMS** — Twilio messaging webhook to the assistant
- **Auth** — login gate with optional “remember me” session cookies

---

## Prerequisites

- **Python 3.10+** (3.11 or 3.12 recommended)
- Accounts & API keys:
  - [Twilio](https://www.twilio.com/) — phone number, Account SID (`AC…`), Auth Token
  - [LiveKit Cloud](https://cloud.livekit.io/) — URL, API key, secret
  - [Deepgram](https://deepgram.com/) — speech-to-text
  - [OpenAI](https://platform.openai.com/) — LLM
  - [Cartesia](https://cartesia.ai/) — text-to-speech
- [ngrok](https://ngrok.com/) (or another HTTPS tunnel) for local Twilio webhooks
- **Git** (optional)

---

## Quick start

### 1. Clone and install

```powershell
git clone https://github.com/Aruho225/NDU-AI.git
cd NDU-AI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

**macOS / Linux:**

```bash
git clone https://github.com/Aruho225/NDU-AI.git
cd NDU-AI

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

```powershell
copy .env.example .env
```

Edit `.env` and fill in your keys. Minimum for voice:

```env
# LiveKit
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
LIVEKIT_AGENT_NAME=ndu-assistant
VOICE_MODE=livekit

# Speech / LLM
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
CARTESIA_API_KEY=...

# Twilio (Account SID must start with AC, not SK)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
TWILIO_WEBHOOK_BASE_URL=https://your-ngrok-url.ngrok-free.app

# Web login
APP_LOGIN_USER=student
APP_LOGIN_PASSWORD=changeme
```

> **Never commit `.env` or `chat_history.db`** — they contain secrets and call data. Both are listed in `.gitignore`.

---

## Running the project

You need **four processes** for full voice (three if you skip the UI). Open a separate terminal for each.

### Terminal 1 — ngrok (public HTTPS for Twilio)

```powershell
ngrok http 8000
```

Copy the **HTTPS** URL (e.g. `https://abcd-1234.ngrok-free.app`) into `.env`:

```env
TWILIO_WEBHOOK_BASE_URL=https://abcd-1234.ngrok-free.app
```

> ngrok free URLs change every restart. Update `.env` and restart the webhook server after each ngrok restart.

### Terminal 2 — Twilio webhook (FastAPI)

```powershell
cd D:\projects\NDU-AI
venv\Scripts\activate
python -m uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000
```

On startup, the server **auto-syncs** your Twilio phone number webhooks from `TWILIO_WEBHOOK_BASE_URL`.

**Health check:**

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/telephony/status
```

### Terminal 3 — LiveKit voice agent

```powershell
cd D:\projects\NDU-AI
venv\Scripts\activate
python agent.py dev
```

Wait until you see `registered worker` with agent name `ndu-assistant` (or your `LIVEKIT_AGENT_NAME`).

### Terminal 4 — Streamlit UI (optional)

```powershell
cd D:\projects\NDU-AI
venv\Scripts\activate
python -m streamlit run ui_app.py
```

Open **http://localhost:8501** and sign in with `APP_LOGIN_USER` / `APP_LOGIN_PASSWORD`.

---

## Helper script (Windows)

Starts the webhook server and LiveKit agent in new windows:

```powershell
.\scripts\start_telephony.ps1
```

You still need **ngrok** and the **Streamlit UI** in separate terminals.

---

## Twilio setup

### Phone number webhooks

For **inbound** calls, Twilio uses the **phone number** config (not the per-call URL used for outbound).

| Setting | URL | Method |
|---------|-----|--------|
| A call comes in | `{TWILIO_WEBHOOK_BASE_URL}/twilio/voice/inbound` | POST |
| Call status changes | `{TWILIO_WEBHOOK_BASE_URL}/twilio/voice/status` | POST |
| Messaging | `{TWILIO_WEBHOOK_BASE_URL}/twilio/webhook` | POST |

**Auto-sync:** restart `uvicorn`, or in the UI go to **Phone numbers → Fix inbound webhook now**.

**Manual:** [Twilio Console](https://console.twilio.com/) → Phone Numbers → your number → Voice & Fax.

### Important

- Use **Webhook** for “A call comes in”, not SIP trunk routing (unless you intentionally use SIP).
- `TWILIO_ACCOUNT_SID` must be the **Account SID** (`AC…`), not an API key (`SK…`).
- Do **not** assign the number to an Elastic SIP trunk if you use the webhook + LiveKit Connector path.

---

## LiveKit setup

This project uses the **Twilio Connector** (Media Streams), not LiveKit SIP trunks.

1. Create a project at [cloud.livekit.io](https://cloud.livekit.io/)
2. Copy **URL**, **API Key**, and **API Secret** into `.env`
3. Set `LIVEKIT_AGENT_NAME=ndu-assistant` (must match the running agent worker)
4. Run `python agent.py dev`

No SIP trunk or dispatch rule is required for the default webhook flow.

---

## Testing

### Inbound call

1. All services running (ngrok, uvicorn, agent)
2. Dial your `TWILIO_PHONE_NUMBER`
3. Webhook terminal should show: `POST /twilio/voice/inbound` → **200 OK**
4. View call + transcript in the UI under **Calls**

### Outbound call

1. Open **Calls** in the UI
2. Enter destination in E.164 format (e.g. `+256700000000`)
3. Click **Start outbound call**

### SMS

Send a text to your Twilio number; the webhook handles it at `/twilio/webhook`.

---

## Architecture

```
Caller ──► Twilio ──► ngrok ──► FastAPI (port 8000)
                                    │
                                    ├─► /twilio/voice/inbound  → LiveKit Connector → Room
                                    ├─► /twilio/voice/outbound → LiveKit Connector → Room
                                    └─► /twilio/webhook        → SMS reply

LiveKit Cloud ◄── agent.py dev (ndu-assistant)
                    Deepgram STT → OpenAI → Cartesia TTS

Streamlit UI (8501) ◄── SQLite (chat_history.db, local only)
```

---

## Project structure

```
NDU-AI/
├── ui_app.py              # Streamlit entry point
├── twilio_webhook.py      # FastAPI Twilio webhooks
├── agent.py               # LiveKit voice agent worker
├── agent_language.py      # Language detection & greetings
├── prompts.py             # System prompts
├── requirements.txt
├── .env.example
├── scripts/
│   └── start_telephony.ps1
└── ui/
    ├── pages/             # Assistant, Calls, Playground, etc.
    ├── sidebar_nav.py     # Navigation
    ├── twilio_phone_setup.py  # Auto-sync Twilio webhooks
    ├── livekit_telephony.py   # LiveKit ↔ Twilio bridge
    └── call_store.py      # Call history (SQLite)
```

---

## Voice modes

| `VOICE_MODE` | Behavior |
|--------------|----------|
| `livekit` (default) | Realtime Deepgram + Cartesia via LiveKit agent |
| `twiml` | Twilio Gather + Polly fallback (no agent worker needed) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Call disconnects immediately | Check webhook logs for **403** — update `TWILIO_WEBHOOK_BASE_URL` and restart uvicorn |
| Inbound never rings / no webhook hit | Sync phone webhook; ensure ngrok points to port **8000** |
| Outbound works, inbound doesn’t | Inbound uses phone number webhook; outbound uses per-call URL — sync inbound separately |
| `api.twilio.com` DNS errors | Network/DNS issue; set DNS to 8.8.8.8 or configure webhook manually in Twilio Console |
| Agent silent on calls | Confirm `python agent.py dev` shows `registered worker` |
| ngrok URL changed | Update `.env` → restart uvicorn (auto-syncs Twilio) |
| Git push blocked for secrets | Never commit `.env` or `chat_history.db` |

---

## Security

- Rotate Twilio Auth Token if credentials were ever exposed
- Keep `.env` local only
- `chat_history.db` stores call metadata locally — do not push to GitHub
- Change default `APP_LOGIN_PASSWORD` before deployment

---

## License

Private / institutional use for Ndejje University AI operations.
