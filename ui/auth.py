import streamlit as st

from ui.auth_brand import render_brand_column
from ui.auth_forms import render_forgot_form, render_login_form, render_register_form
from ui.auth_cookies import clear_auth_token, read_auth_token, save_auth_token
from ui.session_store import create_session_token, resolve_session_token, revoke_session_token
from ui.theme import build_login_css, is_dark_mode, render_theme_toggle
from ui.user_store import init_users_table, seed_admin_from_env

_FORM_RENDERERS = {
    "login": render_login_form,
    "register": render_register_form,
    "forgot": render_forgot_form,
}

REMEMBER_DAYS = 30
SESSION_DAYS = 7


def login(username: str, user_id: int, remember: bool = True, show_flash: bool = True) -> None:
    name = username.strip()
    st.session_state.authenticated = True
    st.session_state.username = name
    st.session_state.user_id = user_id
    if show_flash:
        st.session_state.login_flash = f"Password correct. Welcome back, {name}!"

    days = REMEMBER_DAYS if remember else SESSION_DAYS
    token = create_session_token(user_id, days=days)
    st.session_state.auth_token = token
    save_auth_token(token, days=days)


def logout() -> None:
    token = st.session_state.pop("auth_token", None)
    if token:
        revoke_session_token(token)
    clear_auth_token()
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.session_state.pop("login_flash", None)
    st.session_state.pop("_auth_cookie_ready", None)


def try_restore_session() -> None:
    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        return

    init_users_table()
    token = read_auth_token()
    if not token:
        return

    user = resolve_session_token(token)
    if user:
        st.session_state.authenticated = True
        st.session_state.username = str(user["username"])
        st.session_state.user_id = int(user["user_id"])
        st.session_state.auth_token = token
        return

    clear_auth_token()


def render_login_gate() -> bool:
    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        return True

    init_users_table()
    seed_admin_from_env()
    st.session_state.setdefault("auth_view", "login")

    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    st.markdown(build_login_css(is_dark_mode()), unsafe_allow_html=True)

    brand_col, form_col = st.columns(2, gap="small")
    render_brand_column(brand_col)

    with form_col:
        render_theme_toggle()
        st.markdown('<div class="login-form-col">', unsafe_allow_html=True)
        view = st.session_state.auth_view
        renderer = _FORM_RENDERERS.get(view, render_login_form)
        renderer()

    return False
