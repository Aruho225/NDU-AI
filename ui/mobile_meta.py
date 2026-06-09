VIEWPORT_HTML = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0c2340">
</head><body></body></html>
"""


def inject_mobile_meta() -> None:
    """Inject viewport meta for phones; zero-height iframe avoids layout gap."""
    import streamlit.components.v1 as components

    components.html(VIEWPORT_HTML, height=0, scrolling=False)
