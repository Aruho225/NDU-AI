"""Dark analytics theme for the dashboard (cyan / navy)."""

DASH_BG = "#0b1224"
DASH_PANEL = "#121c36"
DASH_PANEL_2 = "#182444"
DASH_BORDER = "rgba(77, 232, 255, 0.18)"
DASH_TEXT = "#e8f4ff"
DASH_MUTED = "#8ba3c7"
DASH_CYAN = "#00d4ff"
DASH_TEAL = "#00e5c0"
DASH_BLUE = "#3b82f6"
DASH_GLOW = "rgba(0, 212, 255, 0.45)"
DASH_FAIL = "#ff6b8a"
DASH_OK = "#00e5c0"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=DASH_TEXT, family="Segoe UI, sans-serif", size=12),
    margin=dict(l=12, r=12, t=36, b=12),
    xaxis=dict(gridcolor="rgba(139,163,199,0.12)", zerolinecolor="rgba(139,163,199,0.12)"),
    yaxis=dict(gridcolor="rgba(139,163,199,0.12)", zerolinecolor="rgba(139,163,199,0.12)"),
)
