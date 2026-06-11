from ui.dashboard_theme import DASH_BG, DASH_BORDER, DASH_CYAN, DASH_MUTED, DASH_PANEL, DASH_PANEL_2, DASH_TEXT

DASHBOARD_PAGE_CSS = f"""
<style>
    .dash-dark-scope {{
        background: radial-gradient(circle at top right, rgba(0,212,255,0.08), transparent 35%),
                    linear-gradient(180deg, {DASH_BG} 0%, #070d1a 100%);
        border: 1px solid {DASH_BORDER};
        border-radius: 16px;
        padding: 1.1rem 1.15rem 1.35rem;
        margin-bottom: 1rem;
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
    }}
    .dash-topbar {{
        display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;
        padding-bottom: 1rem; margin-bottom: 0.85rem; border-bottom: 1px solid {DASH_BORDER};
    }}
    .dash-eyebrow {{
        margin: 0; font-size: 0.68rem; letter-spacing: 0.14em; text-transform: uppercase;
        color: {DASH_CYAN}; font-weight: 700;
    }}
    .dash-topbar h1 {{
        margin: 0.2rem 0 0; color: {DASH_TEXT}; font-size: 1.55rem; font-weight: 800;
    }}
    .dash-sub {{ margin: 0.35rem 0 0; color: {DASH_MUTED}; font-size: 0.86rem; }}
    .dash-total-pill {{
        min-width: 120px; text-align: center; padding: 0.7rem 1rem; border-radius: 12px;
        background: linear-gradient(180deg, {DASH_PANEL} 0%, {DASH_PANEL_2} 100%);
        border: 1px solid {DASH_BORDER}; box-shadow: 0 0 20px rgba(0,212,255,0.12);
    }}
    .dash-total-pill span {{
        display: block; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: {DASH_MUTED};
    }}
    .dash-total-pill strong {{ display: block; margin-top: 0.2rem; font-size: 1.7rem; color: {DASH_CYAN}; }}
    .dash-toolbar {{
        background: rgba(255,255,255,0.03); border: 1px solid {DASH_BORDER};
        border-radius: 12px; padding: 0.75rem 0.85rem 0.35rem; margin-bottom: 1rem;
    }}
    .dash-section-head {{ margin: 0.15rem 0 0.55rem; }}
    .dash-section-head h2 {{
        margin: 0; color: {DASH_TEXT}; font-size: 0.98rem; font-weight: 800;
        border-left: 3px solid {DASH_CYAN}; padding-left: 0.55rem;
    }}
    .dash-section-head p {{ margin: 0.28rem 0 0 0.7rem; color: {DASH_MUTED}; font-size: 0.78rem; }}
    .dash-chart-label {{
        margin: 0 0 0.35rem; color: {DASH_MUTED}; font-size: 0.76rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.06em;
    }}
    .dash-dark-scope [data-testid="stVerticalBlockBorderWrapper"] {{
        background: linear-gradient(180deg, {DASH_PANEL} 0%, {DASH_PANEL_2} 100%) !important;
        border: 1px solid {DASH_BORDER} !important;
        border-radius: 14px !important;
        padding: 0.75rem 0.85rem 0.9rem !important;
        margin-bottom: 0.9rem !important;
    }}
    .dash-stat-card {{
        display: flex; gap: 0.65rem; align-items: center; height: 100%;
        background: rgba(255,255,255,0.02); border: 1px solid {DASH_BORDER};
        border-radius: 12px; padding: 0.75rem; min-height: 92px;
    }}
    .dash-stat-ring {{
        width: 56px; height: 56px; border-radius: 50%; flex: 0 0 56px;
        background: conic-gradient(var(--ring-color) calc(var(--pct) * 1%), rgba(255,255,255,0.06) 0);
        display: grid; place-items: center; position: relative;
    }}
    .dash-stat-ring::after {{
        content: ""; position: absolute; inset: 8px; border-radius: 50%; background: {DASH_PANEL};
    }}
    .dash-stat-ring span {{
        position: relative; z-index: 1; font-size: 0.72rem; font-weight: 800; color: {DASH_TEXT};
    }}
    .dash-stat-label {{
        margin: 0; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em;
        color: {DASH_MUTED}; font-weight: 700;
    }}
    .dash-stat-value {{ margin: 0.12rem 0 0; font-size: 1.2rem; font-weight: 800; color: {DASH_TEXT}; }}
    .dash-stat-tip-inline {{ margin: 0.15rem 0 0; font-size: 0.68rem; color: {DASH_MUTED}; line-height: 1.3; }}
    .dash-progress {{ margin: 0.45rem 0 0.7rem; }}
    .dash-progress-head {{
        display: flex; justify-content: space-between; color: {DASH_MUTED};
        font-size: 0.76rem; margin-bottom: 0.3rem;
    }}
    .dash-progress-head strong {{ color: {DASH_TEXT}; }}
    .dash-progress-track {{
        height: 9px; border-radius: 999px; background: rgba(255,255,255,0.06); overflow: hidden;
    }}
    .dash-progress-fill {{ height: 100%; border-radius: 999px; }}
    .dash-empty {{
        text-align: center; padding: 2rem 1rem; color: {DASH_MUTED};
        border: 1px dashed {DASH_BORDER}; border-radius: 12px; margin: 0.5rem 0 1rem;
    }}
    .dash-dark-scope .panel-card {{
        background: linear-gradient(180deg, {DASH_PANEL} 0%, {DASH_PANEL_2} 100%);
        border: 1px solid {DASH_BORDER}; border-radius: 14px; padding: 0.9rem 1rem; margin-bottom: 0.85rem;
    }}
    .dash-dark-scope .panel-card h3 {{
        margin: 0 0 0.5rem; color: {DASH_TEXT}; font-size: 0.95rem; font-weight: 800;
        border-left: 3px solid {DASH_CYAN}; padding-left: 0.55rem;
    }}
    .dash-notify {{
        border-radius: 10px; padding: 0.65rem 0.8rem; margin-bottom: 0.4rem;
        border: 1px solid {DASH_BORDER}; background: rgba(255,255,255,0.03);
    }}
    .dash-notify strong {{ display: block; color: {DASH_TEXT}; font-size: 0.84rem; }}
    .dash-notify span {{ display: block; color: {DASH_MUTED}; font-size: 0.76rem; margin-top: 0.12rem; }}
    .dash-notify-alert {{ border-color: rgba(255,107,138,0.45); background: rgba(255,107,138,0.08); }}
    .dash-dark-scope [data-baseweb="tab-list"] {{
        gap: 0.35rem; border-bottom: 1px solid {DASH_BORDER};
    }}
    .dash-dark-scope [data-baseweb="tab"] {{
        background: transparent; color: {DASH_MUTED}; border-radius: 8px 8px 0 0;
    }}
    .dash-dark-scope [data-baseweb="tab"][aria-selected="true"] {{
        color: {DASH_TEXT}; border-bottom: 2px solid {DASH_CYAN};
    }}
</style>
"""
