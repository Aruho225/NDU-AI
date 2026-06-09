from ui.brand_colors import NDU_GOLD, NDU_NAVY, NDU_RED, NDU_SURFACE, NDU_TEXT_MUTED, NDU_WHITE

SESSION_CONTROLS_CSS = f"""
<style>
    .session-status-bar {{
        display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center;
        margin: 0 0 0.85rem 0;
        padding: 0.45rem 0.55rem;
        background: {NDU_WHITE};
        border: 1px solid #d4d4d4;
        border-left: 4px solid {NDU_NAVY};
        border-radius: 6px;
    }}
    .session-status-bar .pill {{
        display: inline-flex; align-items: center; gap: 0.3rem;
        border-radius: 999px; padding: 0.22rem 0.62rem; font-size: 0.74rem; font-weight: 700;
        border: 1px solid transparent;
    }}
    .session-status-bar .pill-live {{
        background: rgba(46, 125, 50, 0.12); color: #1b5e20; border-color: #a5d6a7;
    }}
    .session-status-bar .pill-paused {{
        background: rgba(227, 24, 55, 0.1); color: {NDU_RED}; border-color: rgba(227, 24, 55, 0.35);
    }}
    .session-status-bar .pill-user {{
        background: {NDU_NAVY}; color: {NDU_WHITE}; border-color: {NDU_NAVY};
    }}
    .session-status-bar .pill-voice {{
        background: {NDU_SURFACE}; color: {NDU_NAVY}; border: 1px solid #d4d4d4;
    }}
    .session-status-bar .pill-voice::before {{
        content: "🎙 ";
    }}
</style>
"""
