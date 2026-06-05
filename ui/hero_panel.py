from ndu_links import NDU_ADMISSIONS_PORTAL, NDU_WEBSITE

_HERO_PARTICLES = "".join(
    f'<span style="left:{x}%;top:{y}%;animation-delay:{d}s;"></span>'
    for x, y, d in [(12, 72, 0), (48, 58, 1.2), (76, 80, 2.4), (88, 45, 0.8), (30, 38, 1.8)]
)


def render_hero_html() -> str:
    return f"""
    <div class="hero">
      <div class="hero-orb" aria-hidden="true">
        <span class="hero-orb-glow"></span>
        <span class="hero-orb-core"></span>
      </div>
      <div class="hero-particles" aria-hidden="true">{_HERO_PARTICLES}</div>
      <div class="hero-glass">
        <span class="hero-eyebrow">🎓 Ndejje University</span>
        <h1 class="brand"><span class="brand-accent">NDU</span> AI Assistant</h1>
        <p class="tagline">Your premium gateway for admissions, fees, academics, and ICT support.</p>
        <div class="hero-actions">
          <a class="hero-btn hero-btn-primary" href="{NDU_WEBSITE}" target="_blank" rel="noopener noreferrer">
            🌐 Official website
          </a>
          <a class="hero-btn hero-btn-secondary" href="{NDU_ADMISSIONS_PORTAL}" target="_blank" rel="noopener noreferrer">
            ✍️ Apply online
          </a>
        </div>
        <div class="hero-pills">
          <span class="pill">📋 Admissions</span>
          <span class="pill">💳 Fees</span>
          <span class="pill">📚 Academics</span>
          <span class="pill">🛠️ ICT Help</span>
        </div>
      </div>
    </div>
    """
