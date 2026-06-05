MOBILE_CSS = """
@media (max-width: 768px) {
    .block-container { padding-top: 0.75rem; padding-left: 0.75rem; padding-right: 0.75rem; max-width: 100%; }
    .hero { border-radius: 16px; margin-bottom: 0.65rem; }
    .hero-glass { padding: 0.95rem 1rem 0.85rem; border-radius: 14px; }
    .hero .brand { font-size: 1.5rem; margin-bottom: 0.4rem; }
    .hero .tagline { font-size: 0.88rem; margin-bottom: 0.65rem; }
    .hero-btn { width: 100%; justify-content: center; }
    .hero .pill { font-size: 0.7rem; padding: 0.26rem 0.55rem; }
    .console-bar { gap: 0.35rem; }
    .badge { font-size: 0.72rem; padding: 0.28rem 0.55rem; min-height: 2rem; display: inline-flex; align-items: center; }
    .bg-wave-layer, .ai-ambient .ambient-particle:nth-child(n+5) { display: none; }
    .hero-orb { width: 64px; height: 64px; top: -8px; right: -4px; }
    .ai-ambient { opacity: 0.65; }
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
    .hero-pills .pill { flex: 1 1 calc(50% - 0.35rem); justify-content: center; }
}
@media (hover: none) and (pointer: coarse) {
    .hero-btn:hover, .pill:hover, .user-bubble:hover, .assistant-bubble:hover { transform: none; box-shadow: inherit; }
    .stButton > button:active { transform: scale(0.98); }
}
"""
