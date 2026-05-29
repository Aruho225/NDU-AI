MOBILE_CSS = """
@media (max-width: 768px) {
    .block-container { padding-top: 0.75rem; padding-left: 0.75rem; padding-right: 0.75rem; max-width: 100%; }
    .hero { padding: 0.9rem 1rem; border-radius: 14px; }
    .brand { font-size: 1.55rem; }
    .tagline { font-size: 0.95rem; }
    .pill { font-size: 0.72rem; padding: 0.2rem 0.5rem; margin: 0.12rem 0.25rem 0.12rem 0; }
    .console-bar { gap: 0.35rem; }
    .badge { font-size: 0.72rem; padding: 0.28rem 0.55rem; min-height: 2rem; display: inline-flex; align-items: center; }
    .bg-wave-layer { display: none; }
    .voice-wave-wrap { margin-bottom: 0.6rem; }
    .voice-wave { height: 32px; }
    .voice-wave span { width: 5px; }
    .mobile-tip {
        background: #eff6ff; border: 1px solid #93c5fd; border-radius: 10px;
        padding: 0.65rem 0.8rem; margin-bottom: 0.75rem; font-size: 0.88rem; color: #1e3a8a;
    }
    .stButton > button { min-height: 2.75rem !important; font-size: 0.95rem !important; }
    .stTextArea textarea { font-size: 16px !important; }
    .stTextInput input { font-size: 16px !important; }
    div[data-testid="stHorizontalBlock"]:not(:has(.login-left)) > div[data-testid="column"] {
        width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important;
    }
    section[data-testid="stSidebar"] { min-width: min(85vw, 320px) !important; }
    [data-testid="stMetric"] { padding: 0.25rem 0; }
}
@media (max-width: 480px) {
    .hero .pill { display: inline-block; width: calc(50% - 0.35rem); text-align: center; box-sizing: border-box; }
}
@media (hover: none) and (pointer: coarse) {
    .hero:hover, .pill:hover, .user-bubble:hover, .assistant-bubble:hover { transform: none; box-shadow: inherit; }
    .stButton > button:active { transform: scale(0.98); }
}
"""
