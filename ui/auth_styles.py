from ui.brand_colors import (
    NDU_BORDER,
    NDU_NAVY,
    NDU_NAVY_DARK,
    NDU_PINK,
    NDU_RED,
    NDU_SURFACE,
    NDU_TEXT,
    NDU_TEXT_MUTED,
    NDU_WHITE,
)

LOGIN_CSS = f"""
<style>
    .main {{
        background: {NDU_NAVY_DARK} !important;
    }}
    .login-page .block-container {{
        max-width: 960px !important; padding-top: clamp(1rem, 4vh, 2.2rem) !important;
        padding-bottom: 2rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) {{
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        background: {NDU_WHITE}; border-radius: 6px; overflow: hidden;
        box-shadow: 0 12px 40px rgba(7, 21, 40, 0.25);
        align-items: stretch !important; gap: 0 !important; min-height: 560px;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"] {{
        width: 50% !important; flex: 0 0 50% !important; max-width: 50% !important;
        min-width: 0 !important; padding: 0 !important; min-height: 560px !important;
        display: flex !important; flex-direction: column !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"]:first-child {{
        background: {NDU_NAVY} !important;
        justify-content: center !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"]:last-child {{
        background: {NDU_WHITE} !important;
        justify-content: center !important;
    }}
    .login-left {{
        width: 100%; min-height: 560px; position: relative; overflow: hidden;
        display: flex; align-items: center; justify-content: center;
        background: {NDU_NAVY};
    }}
    .login-left-inner {{
        position: relative; z-index: 2; text-align: center; color: {NDU_WHITE};
        padding: 1.5rem 1.25rem; width: 100%; max-width: 320px; margin: 0 auto;
    }}
    .login-logo {{
        margin: 0 0 0.85rem; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.16em;
        text-transform: uppercase; color: rgba(255,255,255,0.9);
    }}
    .login-badge-frame {{
        background: {NDU_WHITE}; border-radius: 8px; padding: 0.65rem;
        margin: 0 auto 1.1rem; max-width: 190px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }}
    .login-badge-img {{ width: 100%; height: auto; display: block; }}
    .login-left h1 {{
        margin: 0; font-size: clamp(1.2rem, 2.2vw, 1.55rem); font-weight: 800; line-height: 1.2;
        color: {NDU_WHITE};
    }}
    .login-left h1 .accent {{ color: {NDU_RED}; }}
    .login-left .lead {{
        margin: 0.55rem auto 0; font-size: 0.78rem; line-height: 1.5; color: rgba(255,255,255,0.85);
    }}
    .login-left .footnote {{
        margin: 0.75rem 0 0; font-size: 0.72rem; color: rgba(255,255,255,0.7); font-style: italic;
    }}
    .login-waves {{ display: none; }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col {{
        padding: 1.5rem 1.75rem 1.25rem; width: 100%; box-sizing: border-box;
    }}
    .login-form-wrap {{ margin-bottom: 0.35rem; }}
    .login-form-wrap h2 {{
        margin: 0; color: {NDU_NAVY}; font-size: 1.65rem; font-weight: 800;
        border-left: 5px solid {NDU_RED}; padding-left: 0.7rem;
    }}
    .login-form-wrap .subtitle {{
        margin: 0.45rem 0 0 0.95rem; color: {NDU_TEXT_MUTED}; font-size: 0.82rem; line-height: 1.45;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stForm"] {{
        background: {NDU_SURFACE} !important; border: 1px solid {NDU_BORDER} !important; border-radius: 6px !important;
        padding: 0.75rem 1rem 1rem !important; margin-top: 0.5rem !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) label[data-testid="stWidgetLabel"] p {{
        color: {NDU_TEXT} !important; font-size: 0.82rem !important; font-weight: 700 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input {{
        border: 1.5px solid {NDU_BORDER} !important; border-radius: 4px !important;
        padding: 0.62rem 0.75rem !important; background: {NDU_WHITE} !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input:focus {{
        border-color: {NDU_NAVY} !important; background: {NDU_WHITE} !important;
        box-shadow: 0 0 0 2px rgba(12, 35, 64, 0.15) !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stCheckbox label span {{
        color: {NDU_TEXT_MUTED} !important; font-size: 0.84rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] > button,
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] button {{
        background: {NDU_RED} !important;
        color: {NDU_WHITE} !important; border: none !important; border-radius: 4px !important;
        font-weight: 700 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important;
        min-height: 2.8rem !important; margin-top: 0.5rem !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] button:hover {{
        background: {NDU_NAVY} !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col div[data-testid="stHorizontalBlock"] {{
        margin-top: 0.65rem; gap: 0.5rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {{
        background: {NDU_WHITE} !important; color: {NDU_NAVY} !important;
        border: 1.5px solid {NDU_NAVY} !important; border-radius: 4px !important;
        font-weight: 600 !important; min-height: 2.45rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {{
        background: {NDU_SURFACE} !important; color: {NDU_TEXT} !important;
        border: 1.5px solid {NDU_BORDER} !important; border-radius: 4px !important;
        font-weight: 600 !important; min-height: 2.45rem !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > .stButton > button {{
        background: transparent !important; color: {NDU_PINK} !important; border: none !important;
        font-weight: 600 !important; min-height: auto !important; box-shadow: none !important;
    }}
</style>
"""

from ui.auth_styles_mobile import LOGIN_MOBILE_CSS

LOGIN_CSS = LOGIN_CSS.replace("</style>", f"{LOGIN_MOBILE_CSS.strip()}\n</style>")
