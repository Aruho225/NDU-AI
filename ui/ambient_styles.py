AMBIENT_CSS = """
    .ai-ambient {
        position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
    }
    .ai-wave-surface {
        position: absolute; left: -10%; right: -10%; bottom: 8%; height: 42%;
        opacity: 0.35;
        background:
            radial-gradient(ellipse 80% 50% at 50% 100%, rgba(59,130,246,0.18) 0%, transparent 70%),
            repeating-linear-gradient(90deg, transparent 0 48px, rgba(99,102,241,0.04) 48px 49px);
        mask-image: linear-gradient(to top, rgba(0,0,0,0.5), transparent 85%);
    }
    .ai-wave-line {
        position: absolute; left: 0; width: 200%; height: 120px;
        border-radius: 50%; opacity: 0.22;
        border: 1px solid rgba(59, 130, 246, 0.35);
        animation: aiWaveDrift 14s ease-in-out infinite;
    }
    .ai-wave-line:nth-child(1) { bottom: 12%; animation-duration: 16s; }
    .ai-wave-line:nth-child(2) { bottom: 18%; opacity: 0.16; animation-duration: 20s; animation-delay: -4s; }
    .ai-wave-line:nth-child(3) { bottom: 24%; opacity: 0.12; animation-duration: 24s; animation-delay: -8s; }
    .ambient-particle {
        position: absolute; width: 4px; height: 4px; border-radius: 50%;
        background: rgba(99, 102, 241, 0.55);
        box-shadow: 0 0 8px rgba(129, 140, 248, 0.6);
        animation: particleFloat 18s linear infinite;
    }
    .hero { overflow: hidden; }
    .hero-glass { position: relative; z-index: 1; }
    .hero-orb {
        position: absolute; top: -18px; right: -10px; width: 88px; height: 88px;
        pointer-events: none; z-index: 0;
    }
    .hero-orb-core {
        position: absolute; inset: 28%; border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #dbeafe 0%, #3b82f6 45%, #6366f1 100%);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.65);
        animation: orbPulse 3.2s ease-in-out infinite;
    }
    .hero-orb-glow {
        position: absolute; inset: 0; border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,0.45) 0%, transparent 68%);
        filter: blur(6px);
        animation: orbGlow 3.2s ease-in-out infinite;
    }
    .hero-particles { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
    .hero-particles span {
        position: absolute; width: 3px; height: 3px; border-radius: 50%;
        background: rgba(59, 130, 246, 0.5);
        animation: heroParticle 12s ease-in-out infinite;
    }
    .mic-icon {
        display: inline-flex; align-items: center; gap: 0.28rem;
    }
    .mic-icon svg { width: 0.9em; height: 0.9em; flex-shrink: 0; }
    @keyframes aiWaveDrift {
        0%, 100% { transform: translateX(0) scaleY(1); }
        50% { transform: translateX(-12%) scaleY(1.08); }
    }
    @keyframes particleFloat {
        0% { transform: translateY(100vh) translateX(0); opacity: 0; }
        10% { opacity: 0.7; }
        90% { opacity: 0.5; }
        100% { transform: translateY(-10vh) translateX(24px); opacity: 0; }
    }
    @keyframes orbPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }
    @keyframes orbGlow {
        0%, 100% { opacity: 0.55; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.15); }
    }
    @keyframes heroParticle {
        0%, 100% { transform: translateY(0) translateX(0); opacity: 0.2; }
        50% { transform: translateY(-12px) translateX(6px); opacity: 0.85; }
    }
"""
