import streamlit as st

from ui.auth_brand import render_brand_column
from ui.auth_forms import render_forgot_form, render_login_form, render_register_form
from ui.auth_styles import LOGIN_CSS
from ui.user_store import init_users_table, seed_admin_from_env

_FORM_RENDERERS = {
    "login": render_login_form,
    "register": render_register_form,
    "forgot": render_forgot_form,
}


def login(username: str, user_id: int) -> None:
    st.session_state.authenticated = True
    st.session_state.username = username.strip()
    st.session_state.user_id = user_id


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_id = None


def render_login_gate() -> bool:
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
