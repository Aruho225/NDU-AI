LOGIN_DARK_CSS = """
    .login-page .main {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #312e81 100%) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) {
        background: #0f172a !important;
        box-shadow: 0 28px 64px rgba(0, 0, 0, 0.45) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"]:last-child {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    }
    .login-form-wrap h2 { color: #f8fafc !important; border-left-color: #f87171 !important; }
    .login-form-wrap .subtitle { color: #cbd5e1 !important; }
    div[data-testid="stHorizontalBlock"]:has(.login-left) label[data-testid="stWidgetLabel"] p {
        color: #e2e8f0 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stForm"] {
        background: #1e293b !important;
        border-color: #475569 !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input,
    div[data-testid="stHorizontalBlock"]:has(.login-left) input[type="text"],
    div[data-testid="stHorizontalBlock"]:has(.login-left) input[type="password"] {
        background: #0f172a !important;
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
        caret-color: #60a5fa !important;
        border-color: #64748b !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stTextInput input:focus {
        background: #1e293b !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.25) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .stCheckbox label span {
        color: #cbd5e1 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {
        background: #1e293b !important; color: #93c5fd !important; border-color: #475569 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
        background: #292524 !important; color: #fdba74 !important; border-color: #78716c !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col > .stButton > button {
        color: #93c5fd !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) [data-testid="stToggle"] label span {
        color: #e2e8f0 !important;
    }
"""
