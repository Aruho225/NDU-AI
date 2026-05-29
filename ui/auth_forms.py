import streamlit as st

from ui.user_store import authenticate_user, register_user, reset_password


def _set_logged_in(username: str, user_id: int) -> None:
    from ui.auth import login

    login(username, user_id)


def _header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="login-form-wrap">
          <h2>{title}</h2>
          <p class="subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login_form() -> None:
    _header("Login", "Welcome back! Sign in with your registered username and password.")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("User Name", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.checkbox("Remember me", value=True, key="login_remember")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        ok, user_id, message = authenticate_user(username, password)
        if ok and user_id is not None:
            _set_logged_in(username, user_id)
            st.rerun()
        st.error(message)

    c1, c2 = st.columns(2)
    if c1.button("Create account", key="auth_register", use_container_width=True):
        st.session_state.auth_view = "register"
        st.rerun()
    if c2.button("Forgot password?", key="auth_forgot", use_container_width=True):
        st.session_state.auth_view = "forgot"
        st.rerun()


def render_register_form() -> None:
    _header("Sign up", "Create your account to save chats and use the assistant.")
    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("User Name", placeholder="Choose a username")
        email = st.text_input("Email (optional)", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
        submitted = st.form_submit_button("Register", use_container_width=True)

    if submitted:
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, message = register_user(username, password, email)
            if ok:
                st.success(message)
                st.session_state.auth_view = "login"
                st.rerun()
            st.error(message)

    if st.button("Already have an account? Sign in", key="auth_login_from_reg", use_container_width=True):
        st.session_state.auth_view = "login"
        st.rerun()


def render_forgot_form() -> None:
    _header("Reset password", "Enter your username, email, and a new password.")
    with st.form("forgot_form", clear_on_submit=False):
        username = st.text_input("User Name", placeholder="Your username")
        email = st.text_input("Email", placeholder="Email used at registration")
        password = st.text_input("New Password", type="password", placeholder="At least 8 characters")
        confirm = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Update password", use_container_width=True)

    if submitted:
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, message = reset_password(username, email, password)
            if ok:
                st.success(message)
                st.session_state.auth_view = "login"
                st.rerun()
            st.error(message)

    if st.button("Back to sign in", key="auth_login_from_forgot", use_container_width=True):
        st.session_state.auth_view = "login"
        st.rerun()
