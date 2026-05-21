# md-sync-url

Scrape a documentation site and save every page as a Markdown file.
Each URL maps to `output/path/to/page/index.md`, mirroring the site's structure on disk.

## Install

```bash
git clone https://github.com/khangtoh/md_sync_url.git
cd md_sync_url
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

> On Windows use `.venv\Scripts\activate` instead.

## Usage

```bash
md-sync <url> [OPTIONS]
```

### Examples

```bash
# Scrape everything under a URL
md-sync https://example.com/docs/

# Write to a custom folder
md-sync https://example.com/docs/ --output ./my-docs

# Test with a small sample first
md-sync https://example.com/docs/ --max-pages 10

# Politer crawl (slower, fewer parallel requests)
md-sync https://example.com/docs/ --delay 1.0 --concurrency 2
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output / -o` | `output` | Directory to write Markdown files into |
| `--delay / -d` | `0.5` | Seconds to wait between request batches |
| `--concurrency / -c` | `4` | Number of pages to fetch in parallel |
| `--max-pages / -m` | *(none)* | Stop after N pages |

## Output structure

The URL path is mirrored directly onto the filesystem. The root URL's path prefix is stripped, and every page is saved as `index.md` inside a matching folder.

```
output/
├── index.md                    ← /docs/
├── mcp/
│   ├── index.md                ← /docs/mcp/
│   └── quickstart/
│       └── index.md            ← /docs/mcp/quickstart/
└── guide/
    └── intro/
        └── index.md            ← /docs/guide/intro/
```

See [STRUCTURE.md](STRUCTURE.md) for full details on the mapping rules.

## Notes

- Only pages within the root URL prefix are crawled — external links and parent paths are ignored.
- Nav, header, footer, and sidebar elements are stripped before conversion.
- Sites protected by Cloudflare or similar services may block requests from cloud/datacenter IPs. Run the scraper locally if you hit 403 errors.
