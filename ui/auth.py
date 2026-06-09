import time

import streamlit as st

from ui.auth_brand import render_brand_column
from ui.auth_forms import render_forgot_form, render_login_form, render_register_form
from ui.auth_sessions import (
    COOKIE_NAME,
    create_session_token,
    resolve_session_token,
    revoke_session_token,
    session_ttl_days,
)
from ui.auth_styles import LOGIN_CSS
from ui.browser_cookie import erase_browser_cookie, set_browser_cookie
from ui.user_store import init_users_table, seed_admin_from_env

_FORM_RENDERERS = {
    "login": render_login_form,
    "register": render_register_form,
    "forgot": render_forgot_form,
}


def _cached_auth_token() -> str:
    return (st.session_state.get("_auth_cookie_token") or "").strip()


def _cookie_auth_token() -> str:
    try:
        browser_token = (st.context.cookies.get(COOKIE_NAME) or "").strip()
    except Exception:
        browser_token = ""
    return browser_token or _cached_auth_token()


def restore_session_from_cookie() -> bool:
    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        return True

    token = _cookie_auth_token()
    if not token:
        return False

    session = resolve_session_token(token)
    if not session:
        st.session_state._auth_cookie_token = ""
        return False

    login(
        str(session["username"]),
        int(session["user_id"]),
        remember=True,
        persist_cookie=False,
    )
    st.session_state._auth_cookie_token = token
    return True


def login(username: str, user_id: int, remember: bool = True, persist_cookie: bool = True) -> None:
    st.session_state.authenticated = True
    st.session_state.username = username.strip()
    st.session_state.user_id = user_id

    if remember and persist_cookie:
        token = create_session_token(user_id)
        set_browser_cookie(COOKIE_NAME, token, ttl_days=session_ttl_days())
        st.session_state._auth_cookie_token = token


def logout() -> None:
    token = _cookie_auth_token()
    if token:
        revoke_session_token(token)
    erase_browser_cookie(COOKIE_NAME)
    st.session_state._auth_cookie_token = ""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_id = None
    time.sleep(0.3)


def render_login_gate() -> bool:
    restore_session_from_cookie()
    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        return True

    init_users_table()
    seed_admin_from_env()
    st.session_state.setdefault("auth_view", "login")

    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    brand_col, form_col = st.columns(2, gap="small")
    render_brand_column(brand_col)

    with form_col:
        st.markdown('<div class="login-form-col">', unsafe_allow_html=True)
        view = st.session_state.auth_view
        renderer = _FORM_RENDERERS.get(view, render_login_form)
        renderer()

    return False
