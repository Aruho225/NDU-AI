import streamlit as st

from ui.ambient_styles import AMBIENT_CSS
from ui.auth_styles import LOGIN_CSS
from ui.dark_styles import DARK_CSS
from ui.login_dark_styles import LOGIN_DARK_CSS
from ui.hero_styles import HERO_CSS
from ui.styles_mobile import MOBILE_CSS

_BASE_CSS = """
    .main {
        background: radial-gradient(circle at 85% 8%, #e0e7ff 0%, #eff6ff 40%, #f8fafc 100%);
        position: relative;
    }
    .block-container { max-width: 900px; padding-top: 1.5rem; padding-bottom: 2rem; position: relative; z-index: 2; }
    section[data-testid="stSidebar"] { position: relative; z-index: 3; }
    .brand-accent { color: #1d4ed8; }
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
        border-radius: 12px !important; border: 1px solid rgba(29, 78, 216, 0.35) !important;
        background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%) !important;
        box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 3px 10px rgba(29, 78, 216, 0.14) !important;
        transition: transform 150ms ease, box-shadow 150ms ease, background-color 150ms ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 1px 0 rgba(255,255,255,1) inset, 0 8px 20px rgba(29, 78, 216, 0.22) !important;
    }
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
        position: fixed; inset: auto 0 1.2rem 0; display: flex; justify-content: center; pointer-events: none; z-index: 0; opacity: 0.18;
    }
    .bg-wave span {
        width: 12px; border-radius: 999px; background: linear-gradient(180deg, #facc15 0%, #2563eb 45%, #dc2626 100%);
        animation: equalizeBg 1.3s ease-in-out infinite;
    }
    .bg-wave-paused span { animation-play-state: paused; height: 24px; opacity: 0.5; }
    @keyframes softPulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.03); } }
    @keyframes equalize { 0%,100% { height: 12px; } 50% { height: 44px; } }
    @keyframes equalizeBg { 0%,100% { height: 22px; } 50% { height: 110px; } }
"""


def is_dark_mode() -> bool:
    return bool(st.session_state.get("dark_mode", False))


def build_app_css(dark: bool = False) -> str:
    parts = [_BASE_CSS.strip(), HERO_CSS.strip(), AMBIENT_CSS.strip(), MOBILE_CSS.strip()]
    if dark:
        parts.append(DARK_CSS.strip())
    return f"<style>\n{chr(10).join(parts)}\n</style>"


def build_login_css(dark: bool = False) -> str:
    css = LOGIN_CSS.strip()
    if dark:
        css = css.replace("</style>", f"{LOGIN_DARK_CSS.strip()}\n</style>", 1)
    return css


def render_theme_toggle(label: str = "Dark mode", key: str = "dark_mode") -> bool:
    st.session_state.setdefault(key, False)
    return st.toggle(f"🌙 {label}", key=key)
