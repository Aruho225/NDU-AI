"""Backward-compatible hook — sidebar theme lives in sidebar_theme.py."""

from ui.sidebar_theme import inject_sidebar_theme


def inject_ndu_theme() -> None:
    inject_sidebar_theme()
