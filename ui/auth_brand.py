import base64
from pathlib import Path

from ndu_links import NDU_WEBSITE

BADGE_PATH = Path(__file__).resolve().parent / "assets" / "ndu_badge.png"


def _badge_data_uri() -> str:
    encoded = base64.b64encode(BADGE_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


def brand_panel_html() -> str:
    badge = _badge_data_uri()
    return f"""
<div class="login-left">
  <div class="login-left-inner">
    <p class="login-logo">Ndejje University</p>
    <div class="login-badge-frame">
      <img src="{badge}" alt="Ndejje University crest" class="login-badge-img" />
    </div>
    <h1>Welcome to<br><span class="accent">NDU AI Assistant</span></h1>
    <p class="lead">Admissions · Fees · Academics · ICT Support</p>
    <p class="footnote">
      <a href="{NDU_WEBSITE}" target="_blank" rel="noopener noreferrer" style="color:#1e3a8a;font-weight:700;">ndejjeuniversity.ac.ug</a><br>
      Fear of God brings knowledge &amp; wisdom
    </p>
  </div>
  <div class="login-waves" aria-hidden="true">
    <span></span><span></span><span></span>
  </div>
</div>
"""


def render_brand_column(col) -> None:
    col.markdown(brand_panel_html(), unsafe_allow_html=True)
