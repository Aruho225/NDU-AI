APP_CSS = """
<style>
    .main { background: radial-gradient(circle at top right, #fef3c7 0%, #eff6ff 35%, #fee2e2 100%); }
    .block-container { max-width: 900px; padding-top: 1.5rem; padding-bottom: 2rem; position: relative; z-index: 2; }
    section[data-testid="stSidebar"] { position: relative; z-index: 3; }
    .hero {
        background: linear-gradient(135deg, #0f2f79 0%, #1d4ed8 55%, #dc2626 100%);
        border: 2px solid #facc15; border-radius: 18px; padding: 1.1rem 1.25rem; margin-bottom: 1rem; color: #fff;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.2); transition: transform 180ms ease, box-shadow 180ms ease;
    }
    .hero:hover { transform: translateY(-2px); box-shadow: 0 16px 34px rgba(15, 23, 42, 0.28); }
    .brand {
        margin: 0; font-size: clamp(1.8rem, 4.2vw, 2.6rem); font-weight: 800; letter-spacing: 0.03em; line-height: 1.1;
        color: #fff; text-transform: uppercase; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }
    .brand-accent { color: #facc15; }
    .tagline { margin: 0.45rem 0 0.55rem 0; color: #f8fafc; font-weight: 500; }
    .pill {
        display: inline-block; border-radius: 999px; padding: 0.24rem 0.62rem; font-size: 0.8rem; margin: 0.15rem 0.35rem 0.15rem 0;
        background: #facc15; color: #1e3a8a; font-weight: 700; transition: transform 140ms ease, filter 140ms ease;
    }
    .pill:hover { transform: translateY(-1px); filter: brightness(1.03); }
    .console-bar { display: flex; flex-wrap: wrap; gap: 0.45rem; margin: 0.2rem 0 0.8rem 0; }
    .badge {
        background: #1e3a8a; color: #fef3c7; border: 1px solid #facc15; border-radius: 999px; padding: 0.2rem 0.62rem;
        font-size: 0.78rem; font-weight: 700; animation: softPulse 2.2s ease-in-out infinite;
    }
    .user-bubble, .assistant-bubble {
        border-radius: 10px; padding: 0.55rem 0.75rem; transition: transform 160ms ease, box-shadow 160ms ease;
    }
    .user-bubble { background: #fff; border-left: 4px solid #2563eb; }
    .assistant-bubble { background: #fff7ed; border-left: 4px solid #dc2626; margin-top: 0.45rem; }
    .user-bubble, .user-bubble *, .assistant-bubble, .assistant-bubble * { color: #0f172a !important; }
    .assistant-bubble strong { color: #b91c1c !important; }
    .user-bubble:hover, .assistant-bubble:hover { transform: translateY(-1px); box-shadow: 0 8px 16px rgba(30, 58, 138, 0.12); }
    .note { border-left: 4px solid #dc2626; padding: 0.6rem 0.8rem; background: #fff; border-radius: 8px; margin-top: 0.6rem; }
    .stButton > button {
        border-radius: 10px !important; border: 1px solid #1d4ed8 !important;
        transition: transform 150ms ease, box-shadow 150ms ease, background-color 150ms ease !important;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(29, 78, 216, 0.25); }
    .stButton > button:focus { outline: none !important; box-shadow: 0 0 0 0.2rem rgba(250, 204, 21, 0.45) !important; }
    .stTextArea textarea, .stTextInput input {
        transition: border-color 150ms ease, box-shadow 150ms ease; border-radius: 10px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus { box-shadow: 0 0 0 0.18rem rgba(29, 78, 216, 0.22) !important; }
    .voice-wave-wrap { display: flex; align-items: center; gap: 0.55rem; margin: 0.1rem 0 0.9rem 0; }
    .voice-wave { display: flex; align-items: flex-end; gap: 6px; height: 44px; }
    .voice-wave span {
        width: 7px; border-radius: 999px; background: linear-gradient(180deg, #facc15 0%, #dc2626 100%);
        animation: equalize 900ms ease-in-out infinite;
    }
    .voice-wave span:nth-child(2) { animation-delay: 120ms; }
    .voice-wave span:nth-child(3) { animation-delay: 240ms; }
    .voice-wave span:nth-child(4) { animation-delay: 360ms; }
    .voice-wave span:nth-child(5) { animation-delay: 480ms; }
    .voice-wave span:nth-child(6) { animation-delay: 600ms; }
    .voice-wave span:nth-child(7) { animation-delay: 720ms; }
    .voice-wave span:nth-child(8) { animation-delay: 840ms; }
    .wave-paused span { animation-play-state: paused; height: 12px; opacity: 0.55; }
    .wave-live span { opacity: 1; }
    .wave-label { font-size: 0.82rem; font-weight: 700; color: #1e3a8a; }
    .bg-wave-layer {
        position: fixed; inset: auto 0 1.2rem 0; display: flex; justify-content: center; pointer-events: none; z-index: 0;
        opacity: 0.18; filter: blur(0.2px);
    }
    .bg-wave {
        display: flex; align-items: flex-end; gap: 10px; height: 110px; padding: 0.7rem 1rem;
        border-radius: 16px; background: linear-gradient(90deg, rgba(255,255,255,0.05), rgba(30,58,138,0.06), rgba(220,38,38,0.05));
    }
    .bg-wave span {
        width: 12px; border-radius: 999px; background: linear-gradient(180deg, #facc15 0%, #2563eb 45%, #dc2626 100%);
        animation: equalizeBg 1.3s ease-in-out infinite;
    }
    .bg-wave span:nth-child(2) { animation-delay: 120ms; }
    .bg-wave span:nth-child(3) { animation-delay: 220ms; }
    .bg-wave span:nth-child(4) { animation-delay: 350ms; }
    .bg-wave span:nth-child(5) { animation-delay: 460ms; }
    .bg-wave span:nth-child(6) { animation-delay: 580ms; }
    .bg-wave span:nth-child(7) { animation-delay: 700ms; }
    .bg-wave span:nth-child(8) { animation-delay: 820ms; }
    .bg-wave span:nth-child(9) { animation-delay: 930ms; }
    .bg-wave span:nth-child(10) { animation-delay: 1050ms; }
    .bg-wave-paused span { animation-play-state: paused; height: 24px; opacity: 0.5; }
    @keyframes softPulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.03); } }
    @keyframes equalize { 0%,100% { height: 12px; } 50% { height: 44px; } }
    @keyframes equalizeBg { 0%,100% { height: 22px; } 50% { height: 110px; } }
"""

from ui.styles_mobile import MOBILE_CSS

APP_CSS = f"{APP_CSS.strip()}\n{MOBILE_CSS.strip()}\n</style>"
