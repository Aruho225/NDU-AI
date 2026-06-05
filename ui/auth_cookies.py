import datetime

import extra_streamlit_components as stx
import streamlit as st

COOKIE_NAME = "ndu_auth"
_MANAGER_KEY = "ndu_cookie_manager"


def _cookie_manager() -> stx.CookieManager:
    return stx.CookieManager(key=_MANAGER_KEY)


def read_auth_token(*, allow_rerun: bool = True) -> str | None:
    manager = _cookie_manager()
    if not st.session_state.get("_auth_cookie_ready"):
        manager.get_all()
        st.session_state._auth_cookie_ready = True
        if allow_rerun:
            st.rerun()

    token = manager.get(COOKIE_NAME)
    return token or None


def save_auth_token(token: str, days: int = 30) -> None:
    manager = _cookie_manager()
    expires = datetime.datetime.now() + datetime.timedelta(days=days)
    manager.set(
        COOKIE_NAME,
        token,
        key=f"set_{COOKIE_NAME}",
        path="/",
        expires_at=expires,
        same_site="lax",
    )


def clear_auth_token() -> None:
    manager = _cookie_manager()
    manager.delete(COOKIE_NAME, key=f"delete_{COOKIE_NAME}")
