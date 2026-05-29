LOGIN_CSS = """
<style>
    .main {
        background: linear-gradient(135deg, #4f46e5 0%, #2563eb 50%, #7c3aed 100%) !important;
    }
    .login-page .block-container {
        max-width: 960px !important; padding-top: clamp(1rem, 4vh, 2.2rem) !important;
        padding-bottom: 2rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) {
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        background: #fff; border-radius: 22px; overflow: hidden;
        box-shadow: 0 28px 64px rgba(15, 23, 42, 0.22);
        align-items: stretch !important; gap: 0 !important; min-height: 560px;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"] {
        width: 50% !important; flex: 0 0 50% !important; max-width: 50% !important;
        min-width: 0 !important; padding: 0 !important; min-height: 560px !important;
        display: flex !important; flex-direction: column !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"]:first-child {
        background: #87CEEB !important;
        justify-content: center !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"]:last-child {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 55%, #eff6ff 100%) !important;
        justify-content: center !important;
    }
    .login-left {
        width: 100%; min-height: 560px; position: relative; overflow: hidden;
        display: flex; align-items: center; justify-content: center;
        background: #87CEEB;
    }
    .login-left-inner {
        position: relative; z-index: 2; text-align: center; color: #1e3a8a;
        padding: 1.5rem 1.25rem; width: 100%; max-width: 320px; margin: 0 auto;
    }
    .login-logo {
        margin: 0 0 0.85rem; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.16em;
        text-transform: uppercase; color: #1e3a8a;
    }
    .login-badge-frame {
        background: #fff; border-radius: 18px; padding: 0.65rem;
        margin: 0 auto 1.1rem; max-width: 190px;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.2); border: 3px solid #facc15;
    }
    .login-badge-img { width: 100%; height: auto; display: block; }
    .login-left h1 {
        margin: 0; font-size: clamp(1.2rem, 2.2vw, 1.55rem); font-weight: 800; line-height: 1.2;
    }
    .login-left h1 .accent { color: #1d4ed8; }
    .login-left .lead {
        margin: 0.55rem auto 0; font-size: 0.78rem; line-height: 1.5; color: #334155;
    }
    .login-left .footnote {
        margin: 0.75rem 0 0; font-size: 0.72rem; color: #475569; font-style: italic;
    }
    .login-waves {
        position: absolute; left: 0; right: 0; bottom: 0; height: 38%; pointer-events: none; z-index: 1;
    }
    .login-waves span {
        position: absolute; left: -10%; width: 120%; border-radius: 50%; background: rgba(255,255,255,0.35);
    }
    .login-waves span:nth-child(1) { height: 120px; bottom: -35px; }
    .login-waves span:nth-child(2) { height: 160px; bottom: -60px; background: rgba(255,255,255,0.22); }
    .login-waves span:nth-child(3) { height: 200px; bottom: -85px; background: rgba(255,255,255,0.12); }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col {
        padding: 1.5rem 1.75rem 1.25rem; width: 100%; box-sizing: border-box;
    }
    .login-form-wrap { margin-bottom: 0.35rem; }
    .login-form-wrap h2 {
        margin: 0; color: #1e3a8a; font-size: 1.65rem; font-weight: 800;
        border-left: 5px solid #dc2626; padding-left: 0.7rem;
    }
    .login-form-wrap .subtitle {
        margin: 0.45rem 0 0 0.95rem; color: #64748b; font-size: 0.82rem; line-height: 1.45;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stForm"] {
        background: #fff !important; border: 1px solid #bfdbfe !important; border-radius: 14px !important;
        padding: 0.75rem 1rem 1rem !important; margin-top: 0.5rem !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) label[data-testid="stWidgetLabel"] p {
        color: #334155 !important; font-size: 0.82rem !important; font-weight: 700 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input {
        border: 1.5px solid #cbd5e1 !important; border-radius: 8px !important;
        padding: 0.62rem 0.75rem !important; background: #f8fafc !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input:focus {
        border-color: #2563eb !important; background: #fff !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stCheckbox label span {
        color: #475569 !important; font-size: 0.84rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] > button,
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 50%, #dc2626 100%) !important;
        color: #fff !important; border: none !important; border-radius: 10px !important;
        font-weight: 700 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important;
        min-height: 2.8rem !important; margin-top: 0.5rem !important;
        box-shadow: 0 8px 20px rgba(29, 78, 216, 0.3) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col div[data-testid="stHorizontalBlock"] {
        margin-top: 0.65rem; gap: 0.5rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {
        background: #eff6ff !important; color: #1d4ed8 !important;
        border: 1.5px solid #93c5fd !important; border-radius: 10px !important;
        font-weight: 600 !important; min-height: 2.45rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
        background: #fff7ed !important; color: #b45309 !important;
        border: 1.5px solid #fdba74 !important; border-radius: 10px !important;
        font-weight: 600 !important; min-height: 2.45rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > .stButton > button {
        background: transparent !important; color: #2563eb !important; border: none !important;
        font-weight: 600 !important; min-height: auto !important; box-shadow: none !important;
    }
</style>
"""

from ui.auth_styles_mobile import LOGIN_MOBILE_CSS

LOGIN_CSS = LOGIN_CSS.replace("</style>", f"{LOGIN_MOBILE_CSS.strip()}\n</style>")
