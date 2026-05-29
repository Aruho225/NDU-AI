LOGIN_MOBILE_CSS = """
@media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"]:has(.login-left) {
        flex-direction: column !important; flex-wrap: wrap !important; min-height: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.login-left) > div[data-testid="column"] {
        width: 100% !important; flex: 0 0 auto !important; max-width: 100% !important;
        min-height: auto !important;
    }
    .login-left { min-height: 320px; }
    .login-left .footnote { display: none; }
    .login-badge-frame { max-width: 150px; }
    div[data-testid="stHorizontalBlock"]:has(.login-left) .login-form-col {
        padding: 1.2rem 1.1rem 1.1rem;
    }
}
"""
