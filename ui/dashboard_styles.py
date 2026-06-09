from ui.brand_colors import (
    NDU_BORDER,
    NDU_GOLD,
    NDU_NAVY,
    NDU_PINK,
    NDU_RED,
    NDU_SIDEBAR_BORDER,
    NDU_SIDEBAR_MUTED,
    NDU_SIDEBAR_TEXT,
    NDU_SURFACE,
    NDU_TEXT,
    NDU_TEXT_MUTED,
    NDU_WHITE,
)

DASHBOARD_CSS = f"""
<style>
    section[data-testid="stSidebar"] > div {{
        padding-top: 0.25rem;
    }}
    .ndu-sidebar-brand {{
        display: flex; align-items: center; gap: 0.65rem;
        padding: 0.75rem 0.45rem 0.5rem; margin-bottom: 0.15rem;
    }}
    .ndu-sidebar-brand img {{
        width: 40px; height: 40px; border-radius: 8px; background: {NDU_WHITE};
        padding: 2px; border: 2px solid {NDU_GOLD};
    }}
    .ndu-sidebar-brand .title {{
        margin: 0; font-size: 1rem; font-weight: 800; color: {NDU_WHITE}; line-height: 1.15;
    }}
    .ndu-sidebar-brand .subtitle {{
        margin: 0; font-size: 0.65rem; color: {NDU_GOLD}; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em;
    }}
    .ndu-nav-section {{
        margin: 0.75rem 0 0.35rem; padding: 0 0.4rem;
        font-size: 0.65rem; font-weight: 700; color: {NDU_GOLD};
        text-transform: uppercase; letter-spacing: 0.12em;
    }}
    .ndu-sidebar-user {{
        margin: 0.5rem 0.35rem 0;
        padding: 0.55rem 0.65rem;
        background: {NDU_SIDEBAR_BORDER};
        border-radius: 6px;
        border-left: 3px solid {NDU_GOLD};
        font-size: 0.78rem;
        color: {NDU_SIDEBAR_MUTED};
    }}
    .ndu-sidebar-user strong {{
        color: {NDU_SIDEBAR_TEXT};
        font-weight: 700;
    }}

    /* Main workspace */
    .page-header {{
        margin-bottom: 1rem; padding-bottom: 0.75rem;
        border-bottom: 2px solid {NDU_NAVY};
    }}
    .page-header h1 {{
        margin: 0; font-size: 1.45rem; font-weight: 800; color: {NDU_NAVY};
    }}
    .page-header p {{
        margin: 0.35rem 0 0; color: {NDU_TEXT_MUTED}; font-size: 0.9rem;
    }}
    .panel-card {{
        background: {NDU_WHITE}; border: 1px solid {NDU_BORDER}; border-radius: 8px;
        padding: 1rem 1.1rem; margin-bottom: 0.85rem;
        box-shadow: 0 1px 3px rgba(12, 35, 64, 0.06);
    }}
    .panel-card h3 {{
        margin: 0 0 0.5rem; font-size: 0.95rem; font-weight: 800; color: {NDU_NAVY};
        border-left: 3px solid {NDU_RED}; padding-left: 0.55rem;
    }}
    .kv-grid {{
        display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.65rem;
    }}
    .kv-item {{
        background: {NDU_SURFACE}; border: 1px solid {NDU_BORDER}; border-radius: 6px;
        padding: 0.55rem 0.65rem;
    }}
    .kv-item .k {{ font-size: 0.68rem; color: {NDU_TEXT_MUTED}; text-transform: uppercase; letter-spacing: 0.05em; }}
    .kv-item .v {{ font-size: 0.88rem; font-weight: 700; color: {NDU_TEXT}; margin-top: 0.15rem; word-break: break-word; }}
    .status-dot {{
        display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 0.35rem;
    }}
    .status-ok {{ background: #2e7d32; }}
    .status-warn {{ background: {NDU_GOLD}; }}
    .status-off {{ background: #9e9e9e; }}
    .assistant-pill {{
        display: inline-block; border-radius: 999px; padding: 0.18rem 0.55rem; font-size: 0.72rem;
        font-weight: 700; margin: 0.12rem 0.2rem 0.12rem 0; background: {NDU_SURFACE};
        border: 1px solid {NDU_BORDER}; color: {NDU_NAVY};
    }}
    .channel-tag {{
        display: inline-block; background: rgba(12, 35, 64, 0.08); color: {NDU_NAVY};
        border-radius: 4px; border: 1px solid {NDU_BORDER};
        padding: 0.2rem 0.5rem; font-size: 0.75rem; font-weight: 600; margin: 0.15rem 0.25rem 0 0;
    }}
    .phone-card {{
        border: 1px solid {NDU_BORDER}; border-left: 4px solid {NDU_RED};
        border-radius: 8px; padding: 0.9rem 1rem; margin-bottom: 0.75rem;
        background: {NDU_WHITE};
    }}
    .phone-card .number {{
        font-size: 1.15rem; font-weight: 800; color: {NDU_NAVY}; letter-spacing: 0.02em;
    }}
    .list-row-meta {{ font-size: 0.78rem; color: {NDU_TEXT_MUTED}; }}

    /* Streamlit metrics on main pages */
    [data-testid="stMetric"] {{
        background: {NDU_WHITE};
        border: 1px solid {NDU_BORDER};
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
    }}
    [data-testid="stMetricLabel"] {{
        color: {NDU_TEXT_MUTED} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {NDU_NAVY} !important;
    }}
    .live-call-panel {{
        border: 2px solid {NDU_NAVY} !important;
        background: linear-gradient(180deg, #f8fafc 0%, {NDU_WHITE} 100%) !important;
    }}
    .live-call-panel h3 {{
        border-left-color: {NDU_NAVY} !important;
    }}
</style>
"""
