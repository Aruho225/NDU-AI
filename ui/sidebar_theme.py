"""Global sidebar theme injected on every sidebar render."""

from ui.brand_colors import NDU_GOLD, NDU_NAVY, NDU_NAVY_DARK, NDU_RED, NDU_WHITE

_NAV_TEXT = "#d6e8ff"
_NAV_TEXT_HOVER = "#ffffff"

SIDEBAR_THEME_HTML = f"""
<style id="ndu-sidebar-theme-v6">
section[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] [data-testid="stSidebarContent"],
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] .block-container {{
    --background-color: {NDU_NAVY} !important;
    --secondary-background-color: {NDU_NAVY} !important;
    --text-color: {_NAV_TEXT} !important;
    --primary-color: {NDU_RED} !important;
    background-color: {NDU_NAVY} !important;
    background: linear-gradient(180deg, {NDU_NAVY} 0%, {NDU_NAVY_DARK} 100%) !important;
}}

section[data-testid="stSidebar"] {{
    border-right: 3px solid {NDU_RED} !important;
}}

[data-testid="stSidebar"] .ndu-nav-section {{
    color: {NDU_GOLD} !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}}

[data-testid="stSidebar"] .ndu-sidebar-brand {{
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
}}
[data-testid="stSidebar"] .ndu-sidebar-brand::after {{
    content: "";
    display: block;
    height: 3px;
    background: linear-gradient(90deg, {NDU_RED} 0%, {NDU_GOLD} 100%);
    margin-top: 0.65rem;
    border-radius: 2px;
}}
[data-testid="stSidebar"] .ndu-sidebar-brand .title {{
    color: {NDU_WHITE} !important;
}}
[data-testid="stSidebar"] .ndu-sidebar-brand .subtitle {{
    color: {NDU_GOLD} !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: rgba(255, 255, 255, 0.14) !important;
}}

[data-testid="stSidebar"] .ndu-sidebar-user {{
    color: {_NAV_TEXT} !important;
    border-left: 3px solid {NDU_GOLD};
    padding: 0.5rem 0.6rem;
    margin: 0.35rem 0;
    background: rgba(255, 255, 255, 0.06) !important;
    border-radius: 4px;
}}
[data-testid="stSidebar"] .ndu-sidebar-user strong {{
    color: {NDU_WHITE} !important;
}}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    color: {_NAV_TEXT} !important;
}}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {{
    background: {NDU_WHITE} !important;
    color: {NDU_NAVY} !important;
}}

[data-testid="stSidebar"] .stButton {{
    margin-bottom: 0.2rem;
}}
[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255, 255, 255, 0.08) !important;
    color: {_NAV_TEXT} !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button * {{
    color: {_NAV_TEXT} !important;
    -webkit-text-fill-color: {_NAV_TEXT} !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255, 255, 255, 0.14) !important;
    color: {_NAV_TEXT_HOVER} !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
}}

[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {{
    background: {NDU_RED} !important;
    color: {NDU_WHITE} !important;
    border: 1px solid {NDU_RED} !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"] *,
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] *,
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] * {{
    color: {NDU_WHITE} !important;
    -webkit-text-fill-color: {NDU_WHITE} !important;
}}
</style>
"""


def inject_sidebar_theme() -> None:
    import streamlit as st

    st.markdown(SIDEBAR_THEME_HTML, unsafe_allow_html=True)
