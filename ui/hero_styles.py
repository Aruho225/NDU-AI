HERO_CSS = """
    .hero {
        position: relative;
        margin-bottom: 0.85rem;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(135deg, #93c5fd 0%, #c4b5fd 38%, #fda4af 100%);
        box-shadow: 0 4px 24px rgba(30, 58, 138, 0.12), 0 1px 3px rgba(15, 23, 42, 0.06);
    }
    .hero-glass {
        border-radius: 18px;
        padding: 1.15rem 1.35rem 1rem;
        background: linear-gradient(145deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.48) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.65);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }
    .hero-eyebrow {
        display: inline-flex; align-items: center; gap: 0.35rem;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
        color: #1e40af; background: rgba(219, 234, 254, 0.85);
        border: 1px solid rgba(147, 197, 253, 0.5); border-radius: 999px;
        padding: 0.28rem 0.65rem; margin-bottom: 0.65rem;
    }
    .hero .brand {
        margin: 0 0 0.5rem 0;
        font-size: clamp(1.65rem, 3.8vw, 2.35rem);
        font-weight: 800; letter-spacing: 0.04em; line-height: 1.15;
        color: #0f172a; text-transform: uppercase; text-shadow: none;
    }
    .hero .brand-accent {
        color: #1d4ed8;
        background: linear-gradient(120deg, #1d4ed8, #7c3aed);
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero .tagline {
        margin: 0 0 0.85rem 0; color: #475569; font-weight: 500;
        font-size: 0.95rem; line-height: 1.5; max-width: 36rem;
    }
    .hero-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.85rem; }
    .hero-btn {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.52rem 1rem; border-radius: 12px; font-size: 0.84rem; font-weight: 700;
        text-decoration: none; transition: transform 160ms ease, box-shadow 160ms ease;
    }
    .hero-btn-primary {
        color: #fff; background: linear-gradient(180deg, #3b82f6 0%, #1d4ed8 100%);
        border: 1px solid rgba(29, 78, 216, 0.35);
        box-shadow: 0 1px 0 rgba(255,255,255,0.25) inset, 0 4px 14px rgba(29, 78, 216, 0.28);
    }
    .hero-btn-secondary {
        color: #1e3a8a; background: linear-gradient(180deg, #fff 0%, #f1f5f9 100%);
        border: 1px solid rgba(148, 163, 184, 0.45);
        box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 3px 10px rgba(15, 23, 42, 0.08);
    }
    .hero-btn:hover { transform: translateY(-2px); }
    .hero-btn-primary:hover { box-shadow: 0 1px 0 rgba(255,255,255,0.3) inset, 0 8px 20px rgba(29, 78, 216, 0.35); }
    .hero-btn-secondary:hover { box-shadow: 0 1px 0 rgba(255,255,255,1) inset, 0 6px 16px rgba(15, 23, 42, 0.12); }
    .hero-pills { display: flex; flex-wrap: wrap; gap: 0.4rem; }
    .hero .pill {
        display: inline-flex; align-items: center; gap: 0.3rem;
        border-radius: 999px; padding: 0.3rem 0.7rem; font-size: 0.76rem; margin: 0;
        background: rgba(255, 255, 255, 0.75); color: #334155; font-weight: 600;
        border: 1px solid rgba(203, 213, 225, 0.8);
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }
    .hero .pill:hover { transform: translateY(-1px); background: #fff; }
"""
