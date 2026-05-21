# Output Folder Structure

The scraper mirrors a site's URL hierarchy directly onto the filesystem.
Every URL becomes a directory, and the page content is always saved as `index.md` inside it.

## Rule

```
<output>/<path-relative-to-root>/index.md
```

The root URL's path prefix is stripped, then each URL segment becomes a folder.

## Example

Given:

```
md-sync https://example.com/docs/ --output ./output
```

| URL | File |
|-----|------|
| `https://example.com/docs/` | `output/index.md` |
| `https://example.com/docs/mcp/` | `output/mcp/index.md` |
| `https://example.com/docs/mcp/quickstart/` | `output/mcp/quickstart/index.md` |
| `https://example.com/docs/guide/intro/` | `output/guide/intro/index.md` |
| `https://example.com/docs/guide/advanced/` | `output/guide/advanced/index.md` |

Resulting tree:

```
output/
├── index.md                   ← /docs/
├── mcp/
│   ├── index.md               ← /docs/mcp/
│   └── quickstart/
│       └── index.md           ← /docs/mcp/quickstart/
└── guide/
    ├── intro/
    │   └── index.md           ← /docs/guide/intro/
    └── advanced/
        └── index.md           ← /docs/guide/advanced/
```

## Why `index.md`?

Using `index.md` instead of `mcp.md` keeps the structure navigable:

- The folder name (`mcp/`) tells you what the section is.
- `index.md` is the conventional entry point for a directory, matching how web servers serve `index.html`.
- Tools like MkDocs, Docusaurus, and GitHub's file browser treat `index.md` as the section root automatically.

## Scope boundary

The crawler only follows links that stay **within the root URL prefix**.
Links that go to a different domain or a parent path are ignored.

```
root:    https://example.com/docs/
  ✓  https://example.com/docs/mcp/          (same prefix)
  ✓  https://example.com/docs/guide/intro/  (same prefix)
  ✗  https://example.com/blog/              (outside /docs/)
  ✗  https://other.com/docs/               (different domain)
```

## URL normalization

Before writing, each URL is normalized so that trailing slashes and `#fragments`
don't produce duplicate files:

- `https://example.com/docs/mcp` and `https://example.com/docs/mcp/` → same file
- `https://example.com/docs/mcp/#usage` → same file as above (fragment stripped)
