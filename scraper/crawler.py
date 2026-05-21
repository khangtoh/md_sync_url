import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import httpx
from bs4 import BeautifulSoup

from .converter import html_to_markdown
from .writer import url_to_path


def _normalize(url: str) -> str:
    """Strip fragment and normalize trailing slash for deduplication."""
    p = urlparse(url)
    path = p.path if p.path else "/"
    return urlunparse((p.scheme, p.netloc, path, "", "", ""))


async def crawl(
    root_url: str,
    output_dir: Path,
    delay: float = 0.5,
    max_pages: int | None = None,
    concurrency: int = 4,
) -> None:
    root_url = _normalize(root_url)
    root = urlparse(root_url)
    base_prefix = root.scheme + "://" + root.netloc + root.path.rstrip("/")

    visited: set[str] = set()
    queue: asyncio.Queue[str] = asyncio.Queue()
    await queue.put(root_url)

    semaphore = asyncio.Semaphore(concurrency)

    async def fetch_and_process(client: httpx.AsyncClient, url: str) -> list[str]:
        async with semaphore:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
            except Exception as exc:
                print(f"[skip] {url}  ({exc})")
                return []

            content_type = resp.headers.get("content-type", "")
            if "text/html" not in content_type:
                print(f"[skip] {url}  (not HTML: {content_type})")
                return []

            # Write markdown
            md = html_to_markdown(resp.text)
            out = url_to_path(url, root_url, output_dir)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md, encoding="utf-8")
            print(f"[done] {url}  →  {out}")

            # Collect in-scope links
            soup = BeautifulSoup(resp.text, "lxml")
            links: list[str] = []
            for a in soup.find_all("a", href=True):
                abs_url = _normalize(urljoin(url, a["href"]))
                p = urlparse(abs_url)
                full = p.scheme + "://" + p.netloc + p.path.rstrip("/")
                if (
                    p.scheme in ("http", "https")
                    and p.netloc == root.netloc
                    and full.startswith(base_prefix)
                ):
                    links.append(abs_url)

            await asyncio.sleep(delay)
            return links

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=30,
        headers=headers,
    ) as client:
        while not queue.empty():
            if max_pages is not None and len(visited) >= max_pages:
                break

            # Drain up to `concurrency` items at once
            batch: list[str] = []
            while not queue.empty() and len(batch) < concurrency:
                url = await queue.get()
                norm = _normalize(url)
                if norm not in visited:
                    visited.add(norm)
                    batch.append(norm)

            if not batch:
                break

            results = await asyncio.gather(*[fetch_and_process(client, u) for u in batch])
            for links in results:
                for link in links:
                    if link not in visited:
                        await queue.put(link)

    print(f"\nDone. {len(visited)} page(s) processed.")
