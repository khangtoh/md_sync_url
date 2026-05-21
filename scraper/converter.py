import re
from bs4 import BeautifulSoup
import markdownify

# Prefer these selectors for main content, in order
_CONTENT_SELECTORS = [
    "main",
    "article",
    '[role="main"]',
    ".content",
    ".docs-content",
    ".documentation",
    "#content",
    "#main",
]

# Remove these before converting
_NOISE_SELECTORS = [
    "nav",
    "header",
    "footer",
    "aside",
    "script",
    "style",
    ".sidebar",
    ".toc",
    ".nav",
    ".navbar",
    ".breadcrumb",
    '[role="navigation"]',
    '[role="banner"]',
    '[role="complementary"]',
]


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for sel in _NOISE_SELECTORS:
        for el in soup.select(sel):
            el.decompose()

    content = None
    for sel in _CONTENT_SELECTORS:
        content = soup.select_one(sel)
        if content:
            break

    if content is None:
        content = soup.find("body") or soup

    md = markdownify.markdownify(
        str(content),
        heading_style="ATX",
        bullets="-",
        newline_style="backslash",
    )

    # Collapse 3+ consecutive blank lines to 2
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md
