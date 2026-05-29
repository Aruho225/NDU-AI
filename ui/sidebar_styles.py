SIDEBAR_CSS = """
<style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%) !important;
    }
    section[data-testid="stSidebar"] .chats-header {
        display: flex; align-items: center; justify-content: space-between;
        gap: 0.5rem; margin: 0.25rem 0 0.5rem;
    }
    section[data-testid="stSidebar"] .chats-header h3 {
        margin: 0; font-size: 1rem; font-weight: 800; color: #1e3a8a;
    }
    section[data-testid="stSidebar"] .chats-count {
        background: #1d4ed8; color: #fff; font-size: 0.7rem; font-weight: 700;
        border-radius: 999px; padding: 0.15rem 0.5rem; min-width: 1.4rem; text-align: center;
    }
    section[data-testid="stSidebar"] .mobile-tip-box {
        background: #87CEEB; border: 1px solid #5eb3d6; border-radius: 10px;
        padding: 0.45rem 0.55rem; margin-bottom: 0.65rem;
        font-size: 0.72rem; line-height: 1.35; color: #0f2f79;
    }
    section[data-testid="stSidebar"] .chats-empty {
        background: linear-gradient(160deg, #87CEEB 0%, #b3e5fc 100%);
        border: 1px solid #5eb3d6; border-radius: 14px;
        padding: 0.85rem 0.75rem; text-align: center; margin-top: 0.25rem;
    }
    section[data-testid="stSidebar"] .chats-empty img {
        width: 72px; height: auto; display: block; margin: 0 auto 0.55rem;
        background: #fff; border-radius: 12px; padding: 0.35rem;
        border: 2px solid #facc15; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }
    section[data-testid="stSidebar"] .chats-empty strong {
        display: block; color: #0f2f79; font-size: 0.88rem; margin-bottom: 0.25rem;
    }
    section[data-testid="stSidebar"] .chats-empty span {
        color: #1e3a8a; font-size: 0.76rem; line-height: 1.4;
    }
    section[data-testid="stSidebar"] .chat-manage-label {
        margin: 0.65rem 0 0.35rem; font-size: 0.78rem; font-weight: 700; color: #475569;
        text-transform: uppercase; letter-spacing: 0.06em;
    }
    section[data-testid="stSidebar"] [data-testid="stTabs"] button {
        font-size: 0.82rem; font-weight: 700;
    }
    section[data-testid="stSidebar"] .sidebar-nav-active {
        border-color: #1d4ed8 !important;
        background: #eff6ff !important;
    }
</style>
"""
