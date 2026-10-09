#!/usr/bin/env python3
"""Regenerate docs/feed.xml (Atom) and docs/sitemap.xml from the HTML pages.

No dependencies beyond the Python 3 standard library. Run from anywhere:

    python3 scripts/generate_feed_and_sitemap.py

Data comes from each page's <head>:
  - <link rel="canonical">               -> URL (pages without one are skipped)
  - <title>                              -> entry title
  - <meta name="description">            -> entry summary
  - <meta property="article:published_time"> -> marks a page as a post (feed entry)
"""
import html
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

SITE = "https://weekendcodeadventures.xyz/"
DOCS = Path(__file__).resolve().parent.parent / "docs"


def meta(src, pattern):
    m = re.search(pattern, src, re.S)
    return html.unescape(m.group(1)).strip() if m else None


pages = []
for path in sorted(DOCS.glob("*.html")):
    src = path.read_text(encoding="utf-8")
    canonical = meta(src, r'<link rel="canonical" href="([^"]+)"')
    if not canonical:
        print(f"warning: {path.name} has no canonical, skipped", file=sys.stderr)
        continue
    pages.append(
        {
            "url": canonical,
            "title": meta(src, r"<title>(.*?)</title>"),
            "description": meta(src, r'<meta name="description" content="([^"]*)"'),
            "date": meta(src, r'<meta property="article:published_time" content="([^"]+)"'),
        }
    )

posts = sorted((p for p in pages if p["date"]), key=lambda p: p["date"], reverse=True)

# Atom feed
entries = []
for p in posts:
    ts = f"{p['date']}T00:00:00Z"
    entries.append(
        f"""  <entry>
    <title>{escape(p['title'])}</title>
    <link href="{escape(p['url'])}" />
    <id>{escape(p['url'])}</id>
    <published>{ts}</published>
    <updated>{ts}</updated>
    <summary>{escape(p['description'] or '')}</summary>
  </entry>
"""
    )
updated = f"{posts[0]['date']}T00:00:00Z" if posts else "1970-01-01T00:00:00Z"
feed = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Weekend Code Adventures</title>
  <subtitle>Posts by Francesco Barbera</subtitle>
  <link href="{SITE}" />
  <link rel="self" type="application/atom+xml" href="{SITE}feed.xml" />
  <id>{SITE}</id>
  <updated>{updated}</updated>
  <author>
    <name>Francesco Barbera</name>
  </author>
{''.join(entries)}</feed>
"""
(DOCS / "feed.xml").write_text(feed, encoding="utf-8")

# Sitemap
urls = []
for p in sorted(pages, key=lambda p: (p["url"] != SITE, p["url"])):
    lastmod = f"\n    <lastmod>{p['date']}</lastmod>" if p["date"] else ""
    urls.append(f"  <url>\n    <loc>{escape(p['url'])}</loc>{lastmod}\n  </url>\n")
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(urls)}</urlset>
"""
(DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")

print(f"wrote feed.xml ({len(posts)} posts) and sitemap.xml ({len(pages)} urls)")
