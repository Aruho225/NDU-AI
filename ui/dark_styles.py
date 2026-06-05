DARK_CSS = """
    .stApp { background-color: #0b1120 !important; color: #e2e8f0 !important; }
    .main {
        background: radial-gradient(circle at 85% 8%, #1e1b4b 0%, #0f172a 45%, #020617 100%) !important;
        color: #e2e8f0;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    }
    section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    section[data-testid="stSidebar"] [data-testid="stExpander"],
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(165deg, #1e293b 0%, #334155 100%) !important;
        border-color: #475569 !important;
    }
    section[data-testid="stSidebar"] .chats-header h3,
    section[data-testid="stSidebar"] .chats-empty strong { color: #93c5fd !important; }
    section[data-testid="stSidebar"] .mobile-tip-box,
    section[data-testid="stSidebar"] .chats-empty {
        background: #1e293b !important; border-color: #475569 !important; color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] .session-user-chip {
        background: #334155 !important; color: #e2e8f0 !important; border-color: #64748b !important;
    }
    .session-status-bar .pill-live { background: #14532d !important; color: #bbf7d0 !important; }
    .session-status-bar .pill-paused { background: #7f1d1d !important; color: #fecaca !important; }
    .session-status-bar .pill-user { background: #1e3a8a !important; color: #dbeafe !important; }
    .session-status-bar .pill-voice { background: #713f12 !important; color: #fef08a !important; }
    .user-bubble { background: #1e293b !important; border-left-color: #60a5fa !important; }
    .assistant-bubble { background: #292524 !important; border-left-color: #f87171 !important; }
    .user-bubble, .user-bubble *, .assistant-bubble, .assistant-bubble * { color: #f1f5f9 !important; }
    .assistant-bubble strong { color: #fca5a5 !important; }
    .note { background: #1e293b !important; color: #e2e8f0 !important; border-left-color: #f87171 !important; }
    .badge { background: #1e3a8a !important; color: #fef3c7 !important; }
    .wave-label { color: #93c5fd !important; }
    .mobile-tip { background: #1e293b !important; border-color: #475569 !important; color: #cbd5e1 !important; }
    .hero { background: linear-gradient(135deg, #312e81 0%, #4c1d95 38%, #7f1d1d 100%) !important; }
    .hero-glass {
        background: linear-gradient(145deg, rgba(30,41,59,0.88) 0%, rgba(15,23,42,0.72) 100%) !important;
        border-color: rgba(100, 116, 139, 0.45) !important;
    }
    .hero .brand { color: #f8fafc !important; }
    .hero .tagline { color: #94a3b8 !important; }
    .hero-eyebrow { background: rgba(30, 58, 138, 0.5) !important; color: #bfdbfe !important; }
    .hero .pill { background: rgba(51, 65, 85, 0.85) !important; color: #e2e8f0 !important; border-color: #64748b !important; }
    .hero-btn-secondary { background: linear-gradient(180deg, #334155 0%, #1e293b 100%) !important; color: #e2e8f0 !important; }
    .ai-wave-surface { opacity: 0.2 !important; }
    .stButton > button {
        background: linear-gradient(180deg, #334155 0%, #1e293b 100%) !important;
        color: #f1f5f9 !important; border-color: #475569 !important;
    }
    [data-testid="stMetric"] { background: #1e293b; border-radius: 10px; padding: 0.35rem; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1e293b !important; color: #f1f5f9 !important; border-color: #475569 !important;
    }
    .main h1, .main h2, .main h3, .main h4, .main p, .main label, .main .stCaption { color: #e2e8f0 !important; }
    div[data-testid="stForm"] { border-color: #475569 !important; background: #0f172a !important; }
    .stTextArea textarea, .stTextInput input {
        color: #f8fafc !important;
        -webkit-text-fill-color: #f8fafc !important;
        caret-color: #60a5fa !important;
    }
"""
