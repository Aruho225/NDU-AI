"""Set and clear browser cookies from Streamlit (read via st.context.cookies on reload)."""

from __future__ import annotations

import json

import streamlit.components.v1 as components


def set_browser_cookie(name: str, value: str, ttl_days: int = 30) -> None:
    payload = json.dumps({"name": name, "value": value, "days": ttl_days})
    components.html(
        f"""
        <script>
        (function () {{
          const cfg = {payload};
          const date = new Date();
          date.setTime(date.getTime() + (cfg.days * 24 * 60 * 60 * 1000));
          const expires = "; expires=" + date.toUTCString();
          document.cookie = cfg.name + "=" + encodeURIComponent(cfg.value) + expires + "; path=/; SameSite=Lax";
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def erase_browser_cookie(name: str) -> None:
    payload = json.dumps(name)
    components.html(
        f"""
        <script>
        (function () {{
          const name = {payload};
          document.cookie = name + "=; Max-Age=0; path=/; SameSite=Lax";
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
