from ui.brand_colors import (
    NDU_BG,
    NDU_BORDER,
    NDU_BORDER_LIGHT,
    NDU_NAVY,
    NDU_PINK,
    NDU_RED,
    NDU_SURFACE,
    NDU_TEXT,
    NDU_TEXT_MUTED,
    NDU_WHITE,
)

APP_CSS = f"""
<style>
    .main {{ background: {NDU_BG}; }}
    .block-container {{ max-width: 1100px; padding-top: 1.25rem; padding-bottom: 2rem; position: relative; z-index: 2; }}
    section[data-testid="stSidebar"] {{ position: relative; z-index: 3; }}
    .hero {{
        background: {NDU_NAVY};
        border-bottom: 4px solid {NDU_RED};
        border-radius: 4px; padding: 1.1rem 1.25rem; margin-bottom: 1rem; color: {NDU_WHITE};
        box-shadow: 0 4px 14px rgba(7, 21, 40, 0.15);
    }}
    .brand {{
        margin: 0; font-size: clamp(1.8rem, 4.2vw, 2.6rem); font-weight: 800; letter-spacing: 0.03em; line-height: 1.1;
        color: {NDU_WHITE}; text-transform: uppercase;
    }}
    .brand-accent {{ color: {NDU_RED}; }}
    .tagline {{ margin: 0.45rem 0 0.55rem 0; color: rgba(255,255,255,0.92); font-weight: 500; }}
    .pill {{
        display: inline-block; border-radius: 999px; padding: 0.24rem 0.62rem; font-size: 0.8rem; margin: 0.15rem 0.35rem 0.15rem 0;
        background: rgba(255,255,255,0.12); color: {NDU_WHITE}; border: 1px solid rgba(255,255,255,0.35); font-weight: 600;
    }}
    .console-bar {{ display: flex; flex-wrap: wrap; gap: 0.45rem; margin: 0.2rem 0 0.8rem 0; }}
    .badge {{
        background: {NDU_WHITE}; color: {NDU_NAVY}; border: 1px solid {NDU_BORDER};
        border-radius: 999px; padding: 0.2rem 0.62rem; font-size: 0.78rem; font-weight: 700;
    }}
    .user-bubble, .assistant-bubble {{
        border-radius: 6px; padding: 0.55rem 0.75rem;
    }}
    .user-bubble {{ background: {NDU_WHITE}; border-left: 4px solid {NDU_NAVY}; border: 1px solid {NDU_BORDER_LIGHT}; border-left: 4px solid {NDU_NAVY}; }}
    .assistant-bubble {{ background: {NDU_SURFACE}; border: 1px solid {NDU_BORDER_LIGHT}; border-left: 4px solid {NDU_RED}; margin-top: 0.45rem; }}
    .user-bubble, .user-bubble *, .assistant-bubble, .assistant-bubble * {{ color: {NDU_TEXT} !important; }}
    .assistant-bubble strong {{ color: {NDU_NAVY} !important; }}
    .note {{ border-left: 4px solid {NDU_RED}; padding: 0.6rem 0.8rem; background: {NDU_WHITE}; border-radius: 4px; margin-top: 0.6rem; color: {NDU_TEXT_MUTED}; }}
    .main .stButton > button {{
        border-radius: 6px !important;
        border: 1px solid {NDU_NAVY} !important;
        color: {NDU_NAVY} !important;
        background: {NDU_WHITE} !important;
        font-weight: 600 !important;
    }}
    .main .stButton > button:hover {{
        background: {NDU_NAVY} !important;
        color: {NDU_WHITE} !important;
        box-shadow: none !important;
        transform: none !important;
    }}
    .main .stButton > button[kind="primary"],
    .main .stButton > button[data-testid="stBaseButton-primary"] {{
        background: {NDU_NAVY} !important;
        border-color: {NDU_NAVY} !important;
        color: {NDU_WHITE} !important;
    }}
    .main .stButton > button[kind="primary"]:hover,
    .main .stButton > button[data-testid="stBaseButton-primary"]:hover {{
        background: #0a1a30 !important;
        color: {NDU_WHITE} !important;
    }}
    .stTextArea textarea, .stTextInput input {{
        border-radius: 4px !important; border-color: {NDU_BORDER} !important;
    }}
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: {NDU_NAVY} !important;
        box-shadow: 0 0 0 2px rgba(12, 35, 64, 0.15) !important;
    }}
    .main [data-testid="stFormSubmitButton"] > button,
    .main [data-testid="stFormSubmitButton"] button,
    .main [data-testid="stForm"] .stButton > button {{
        background: {NDU_NAVY} !important;
        color: {NDU_WHITE} !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
    }}
    .main [data-testid="stFormSubmitButton"] > button:hover,
    .main [data-testid="stFormSubmitButton"] button:hover {{
        background: #0a1a30 !important;
        color: {NDU_WHITE} !important;
    }}
    .voice-wave-wrap {{ display: flex; align-items: center; gap: 0.55rem; margin: 0.1rem 0 0.9rem 0; }}
    .voice-wave {{ display: flex; align-items: flex-end; gap: 6px; height: 44px; }}
    .voice-wave span {{
        width: 7px; border-radius: 999px; background: {NDU_RED};
        animation: equalize 900ms ease-in-out infinite;
    }}
    .voice-wave span:nth-child(2) {{ animation-delay: 120ms; }}
    .voice-wave span:nth-child(3) {{ animation-delay: 240ms; }}
    .voice-wave span:nth-child(4) {{ animation-delay: 360ms; }}
    .voice-wave span:nth-child(5) {{ animation-delay: 480ms; }}
    .voice-wave span:nth-child(6) {{ animation-delay: 600ms; }}
    .voice-wave span:nth-child(7) {{ animation-delay: 720ms; }}
    .voice-wave span:nth-child(8) {{ animation-delay: 840ms; }}
    .wave-paused span {{ animation-play-state: paused; height: 12px; opacity: 0.45; }}
    .wave-live span {{ opacity: 1; }}
    .wave-label {{ font-size: 0.82rem; font-weight: 700; color: {NDU_NAVY}; }}
    .bg-wave-layer {{ display: none; }}
    @keyframes equalize {{ 0%,100% {{ height: 12px; }} 50% {{ height: 44px; }} }}
"""

from ui.styles_mobile import MOBILE_CSS

APP_CSS = f"{APP_CSS.strip()}\n{MOBILE_CSS.strip()}\n</style>"
