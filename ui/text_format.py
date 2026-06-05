import html
import re

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def format_chat_html(text: str) -> str:
    """Escape chat text for HTML; turn **bold** into <strong> without showing stars."""
    parts: list[str] = []
    last = 0
    for match in _BOLD_RE.finditer(text):
        parts.append(html.escape(text[last : match.start()]))
        parts.append(f"<strong>{html.escape(match.group(1))}</strong>")
        last = match.end()
    parts.append(html.escape(text[last:]))
    return "".join(parts).replace("\n", "<br>")
