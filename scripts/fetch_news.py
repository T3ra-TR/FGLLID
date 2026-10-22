#!/usr/bin/env python3
"""Fetch official FGLLID news from mol.gov.mm WordPress API into data/news.json."""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "news.json"

API = "https://www.mol.gov.mm/wp-json/wp/v2/posts"
# Official categories on mol.gov.mm
CAT_FGLLID_NEWS = 31  # news-fgllid
CAT_BREAKING = 73  # breaking-news
CAT_FGLLID_ANN = 98  # fgllid-announcement

UA = "FGLLID-Website/1.0 (local news sync; +https://www.mol.gov.mm)"


def strip_html(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_posts(category: int, per_page: int = 12) -> list[dict]:
    qs = urllib.parse.urlencode(
        {
            "categories": category,
            "per_page": per_page,
            "_embed": "1",
            "orderby": "date",
            "order": "desc",
        }
    )
    req = urllib.request.Request(
        f"{API}?{qs}",
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def normalize(post: dict) -> dict:
    media = (post.get("_embedded") or {}).get("wp:featuredmedia") or []
    image = None
    if media:
        image = media[0].get("source_url") or media[0].get("media_details", {}).get(
            "sizes", {}
        ).get("medium_large", {}).get("source_url")

    authors = (post.get("_embedded") or {}).get("author") or []
    author = strip_html(authors[0].get("name", "")) if authors else "MOL"

    return {
        "id": post.get("id"),
        "title": strip_html((post.get("title") or {}).get("rendered", "")),
        "excerpt": strip_html((post.get("excerpt") or {}).get("rendered", "")),
        "date": (post.get("date") or "")[:10],
        "datetime": post.get("date"),
        "link": post.get("link"),
        "image": image,
        "author": author or "Web Admin",
    }


def main() -> int:
    try:
        news_raw = fetch_posts(CAT_FGLLID_NEWS, 12)
    except urllib.error.URLError as exc:
        print(f"Failed to fetch FGLLID news: {exc}")
        return 1

    try:
        breaking_raw = fetch_posts(CAT_BREAKING, 8)
    except urllib.error.URLError:
        breaking_raw = []

    try:
        ann_raw = fetch_posts(CAT_FGLLID_ANN, 6)
    except urllib.error.URLError:
        ann_raw = []

    news = [normalize(p) for p in news_raw]
    breaking = [normalize(p) for p in breaking_raw]
    announcements = [normalize(p) for p in ann_raw]

    # Ticker prefers FGLLID announcements, else breaking, else news titles
    ticker_source = announcements or breaking or news
    ticker = [item["title"] for item in ticker_source if item.get("title")][:8]

    payload = {
        "source": "https://www.mol.gov.mm/",
        "fgllidNewsUrl": "https://www.mol.gov.mm/category/news-fgllid/",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "ticker": ticker,
        "items": news,
        "announcements": announcements,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(news)} FGLLID news + {len(ticker)} ticker items -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
