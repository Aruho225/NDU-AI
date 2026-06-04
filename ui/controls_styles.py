SESSION_CONTROLS_CSS = """
<style>
    section[data-testid="stSidebar"] [data-testid="stExpander"] {
        background: linear-gradient(165deg, #87CEEB 0%, #b3e5fc 100%) !important;
        border-color: #5eb3d6 !important;
        border-radius: 14px !important;
        margin-bottom: 0.85rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #0f2f79 !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(165deg, #87CEEB 0%, #b3e5fc 100%) !important;
        border-color: #5eb3d6 !important; border-radius: 14px !important;
        padding: 0.35rem 0.5rem 0.5rem !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 6px 16px rgba(30, 58, 138, 0.12);
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] p,
    section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] label {
        color: #0f2f79 !important;
    }
    section[data-testid="stSidebar"] .session-user-chip {
        display: inline-block; background: #fff; color: #1e3a8a; border-radius: 999px;
        padding: 0.2rem 0.65rem; font-size: 0.72rem; font-weight: 700; margin-bottom: 0.55rem;
        border: 1px solid #93c5fd;
    }
    section[data-testid="stSidebar"] .session-panel-wrap [data-testid="stVerticalBlock"] {
        gap: 0.35rem;
    }
    .session-status-bar {
        display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center;
        margin: 0 0 0.85rem 0;
    }
    .session-status-bar .pill {
        display: inline-flex; align-items: center; gap: 0.3rem;
        border-radius: 999px; padding: 0.22rem 0.62rem; font-size: 0.74rem; font-weight: 700;
        border: 1px solid transparent;
    }
    .session-status-bar .pill-live { background: #dcfce7; color: #166534; border-color: #86efac; }
    .session-status-bar .pill-paused { background: #fee2e2; color: #991b1b; border-color: #fca5a5; }
    .session-status-bar .pill-user { background: #e0f2fe; color: #1e3a8a; border-color: #7dd3fc; }
    .session-status-bar .pill-voice { background: #fef9c3; color: #854d0e; border-color: #fde047; }
</style>
"""
