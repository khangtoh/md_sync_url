from pathlib import Path
from urllib.parse import urlparse


def url_to_path(url: str, root_url: str, output_dir: Path) -> Path:
    """
    Map a URL to an output file path, always named index.md.

    Example:
        root_url  = https://example.com/docs/
        url       = https://example.com/docs/guide/intro/
        output    = output/guide/intro/index.md
    """
    root_path = urlparse(root_url).path.rstrip("/")
    url_path = urlparse(url).path.rstrip("/")

    if url_path.startswith(root_path):
        rel = url_path[len(root_path):]
    else:
        rel = url_path

    rel = rel.strip("/")
    if rel:
        return output_dir / rel / "index.md"
    return output_dir / "index.md"
