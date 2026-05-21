"""Unit tests — no network required."""
from pathlib import Path
import textwrap

from scraper.converter import html_to_markdown
from scraper.writer import url_to_path


HTML = textwrap.dedent("""\
    <html>
    <head><title>Guide</title></head>
    <body>
      <nav><a href="/">Home</a></nav>
      <main>
        <h1>Getting Started</h1>
        <p>Install the package with <code>pip install foo</code>.</p>
        <h2>Next Steps</h2>
        <ul>
          <li><a href="/docs/advanced/">Advanced guide</a></li>
        </ul>
      </main>
      <footer>Copyright 2024</footer>
    </body>
    </html>
""")


def test_html_to_markdown_strips_nav_footer():
    md = html_to_markdown(HTML)
    assert "Home" not in md           # nav stripped
    assert "Copyright" not in md      # footer stripped
    assert "# Getting Started" in md
    assert "pip install foo" in md


def test_html_to_markdown_heading_levels():
    md = html_to_markdown(HTML)
    assert "# Getting Started" in md
    assert "## Next Steps" in md


def test_url_to_path_root(tmp_path):
    root = "https://example.com/docs/"
    url = "https://example.com/docs/"
    assert url_to_path(url, root, tmp_path) == tmp_path / "index.md"


def test_url_to_path_subpage(tmp_path):
    root = "https://example.com/docs/"
    url = "https://example.com/docs/guide/intro/"
    assert url_to_path(url, root, tmp_path) == tmp_path / "guide" / "intro" / "index.md"


def test_url_to_path_no_trailing_slash(tmp_path):
    root = "https://example.com/docs/"
    url = "https://example.com/docs/mcp"
    assert url_to_path(url, root, tmp_path) == tmp_path / "mcp" / "index.md"
