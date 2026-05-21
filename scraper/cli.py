import asyncio
from pathlib import Path

import click

from .crawler import crawl


@click.command()
@click.argument("url")
@click.option("--output", "-o", default="output", show_default=True, help="Output directory")
@click.option("--delay", "-d", default=0.5, show_default=True, help="Seconds between requests")
@click.option("--concurrency", "-c", default=4, show_default=True, help="Parallel fetches")
@click.option("--max-pages", "-m", default=None, type=int, help="Stop after N pages")
def main(url: str, output: str, delay: float, concurrency: int, max_pages: int | None) -> None:
    """Scrape a docs site and write each page as output/path/to/page/index.md."""
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    asyncio.run(crawl(url, output_dir, delay=delay, max_pages=max_pages, concurrency=concurrency))
