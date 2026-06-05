_MIC_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11h-2z"/>'
    "</svg>"
)


def mic_label(text: str) -> str:
    return f'<span class="mic-icon">{_MIC_SVG}<span>{text}</span></span>'


def render_ambient_html() -> str:
    particles = "".join(
        f'<span class="ambient-particle" style="left:{left}%;animation-delay:{delay}s;'
        f'animation-duration:{dur}s;"></span>'
        for left, delay, dur in [
            (8, 0, 16), (22, 3, 19), (41, 1, 17), (63, 5, 21),
            (78, 2, 18), (91, 6, 20), (35, 4, 22), (55, 7, 15),
        ]
    )
    return f"""
    <div class="ai-ambient" aria-hidden="true">
      <div class="ai-wave-surface"></div>
      <div class="ai-wave-line"></div>
      <div class="ai-wave-line"></div>
      <div class="ai-wave-line"></div>
      {particles}
    </div>
    """
