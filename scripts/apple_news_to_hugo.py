#!/usr/bin/env python3
"""
Quét RSS của Apple, tạo bài Hugo trong content/post/ khi có:
- Bản Xcode mới (feed Releases — tiêu đề bắt đầu bằng "Xcode ").
- Cập nhật chính sách App Store / thỏa thuận (feed News — lọc theo tiêu đề mô tả bên dưới).

Lần chạy đầu (chưa có file state): chỉ khởi tạo state, KHÔNG tạo bài (tránh flood bài cũ).
Chạy lần sau: mỗi mục RSS mới (guid chưa thấy) → một thư mục bài viết mới.

Chạy: python3 scripts/apple_news_to_hugo.py
Biến môi trường tùy chọn:
  APPLE_POST_DRAFT=1  → front matter draft: true
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_POST = REPO_ROOT / "content" / "post"
STATE_PATH = REPO_ROOT / "data" / "apple-feed-state.json"

RELEASES_RSS = "https://developer.apple.com/news/releases/rss/releases.rss"
NEWS_RSS = "https://developer.apple.com/news/rss/news.rss"

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}

# Tiêu đề tin News coi là “chính sách / thỏa thuận App Store” (chữ thường khi so khớp).
POLICY_TITLE_KEYWORDS = (
    "app review guideline",
    "developer program license agreement",
    "agreements and guidelines",
    "updated guidelines now available",
    "license agreement now available",
)


def _fetch_rss(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "hieneo-apple-feed-sync/1.0 (+local; Hugo blog)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _absolutize_apple_href(href: str) -> str:
    href = href.strip()
    if href.startswith(("http://", "https://")):
        return href
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return "https://developer.apple.com" + href
    return "https://developer.apple.com/" + href.lstrip("/")


def _strip_html(raw: str) -> str:
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r"(?s)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?s)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _parse_pub_date(pub: str | None) -> datetime:
    if not pub:
        return datetime.now(timezone.utc)
    try:
        dt = parsedate_to_datetime(pub)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def _yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _slug_part(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:80] if s else "item"


def _parse_rss_items(xml_text: str) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []
    out: list[dict[str, Any]] = []
    for item in channel.findall("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        guid_el = item.find("guid")
        desc_el = item.find("description")
        pub_el = item.find("pubDate")
        enc_el = item.find("content:encoded", NS)
        title = (title_el.text or "").strip() if title_el is not None else ""
        link = (link_el.text or "").strip() if link_el is not None else ""
        guid = (guid_el.text or link or title).strip() if guid_el is not None else link or title
        desc = (desc_el.text or "").strip() if desc_el is not None else ""
        encoded = (enc_el.text or "").strip() if enc_el is not None else ""
        out.append(
            {
                "title": title,
                "link": link,
                "guid": guid,
                "description": desc,
                "encoded": encoded,
                "pubDate": (pub_el.text or "").strip() if pub_el is not None else "",
            }
        )
    return out


def _is_xcode_release(item: dict[str, Any]) -> bool:
    t = item["title"]
    return bool(re.match(r"^Xcode\s", t, re.I))


def _is_policy_news(item: dict[str, Any]) -> bool:
    t = item["title"].lower()
    return any(k in t for k in POLICY_TITLE_KEYWORDS)


def _classify(item: dict[str, Any], source: str) -> str | None:
    if source == "releases" and _is_xcode_release(item):
        return "xcode"
    if source == "news" and _is_policy_news(item):
        return "policy"
    return None


def _post_folder_name(kind: str, item: dict[str, Any]) -> str:
    """Tên thư mục duy nhất, ổn định theo guid."""
    parsed = urlparse(item["link"])
    qs_id = ""
    if parsed.query:
        for part in parsed.query.split("&"):
            if part.startswith("id="):
                qs_id = _slug_part(part[3:])
                break
    tail = qs_id or _slug_part(item["guid"])
    base = _slug_part(item["title"])[:50]
    return f"apple-{kind}-{base}-{tail}".strip("-")


def _build_markdown(kind: str, item: dict[str, Any]) -> str:
    dt = _parse_pub_date(item.get("pubDate"))
    date_str = dt.date().isoformat()
    title = item["title"]
    link = item["link"]
    excerpt = _strip_html(item["description"] + " " + item["encoded"])[:320]
    if len(excerpt) > 300:
        excerpt = excerpt[:297] + "…"

    extra_link = ""
    if kind == "xcode":
        rn = None
        enc = item.get("encoded") or ""
        for m in re.finditer(r'href=(["\']?)([^"\'>\s]+)\1', enc):
            href = m.group(2)
            if "xcode" in href.lower() and "-rn" in href.lower():
                rn = _absolutize_apple_href(href)
                break
        if rn:
            extra_link = f"\n- [Release notes (Apple)]({rn})"

    if kind == "xcode":
        tags = "    - Xcode\n    - Apple\n    - release-notes\n    - apple-rss"
        desc_ym = f"Bản Xcode mới trên Apple Developer Releases — {title}. Xem link chính thức và release notes bên dưới."
    else:
        tags = "    - App Store\n    - Apple\n    - policy\n    - apple-rss"
        desc_ym = f"Cập nhật chính sách / thỏa thuận từ Apple Developer News — {title}. Đọc toàn văn trên trang Apple."

    draft = os.environ.get("APPLE_POST_DRAFT", "").lower() in ("1", "true", "yes")
    draft_line = "draft: true\n" if draft else ""

    body = f"""Apple đăng thông báo sau (RSS). Đây là bản ghi tự động — bạn có thể bổ sung phân tích tiếng Việt phía dưới.

- [Xem bài gốc trên Apple Developer]({link}){extra_link}

<!--more-->

## Tóm tắt nhanh

**Tiêu đề (EN):** {title}

**Ngày (theo RSS):** {item.get("pubDate") or "—"}

**Trích đoạn:** {excerpt or "—"}
"""
    return f"""---
title: "{_yaml_escape(title)}"
date: {date_str}
description: "{_yaml_escape(desc_ym)}"
categories:
    - iOS
tags:
{tags}
{draft_line}---

{body}
"""


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"seen_guids": []}
    with open(STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> int:
    seen: set[str] = set(load_state().get("seen_guids", []))
    bootstrap = len(seen) == 0

    feeds: list[tuple[str, str]] = [
        ("releases", RELEASES_RSS),
        ("news", NEWS_RSS),
    ]

    collected: list[tuple[str, dict[str, Any]]] = []
    for source, url in feeds:
        try:
            xml_text = _fetch_rss(url)
        except Exception as e:
            print(f"Lỗi tải {url}: {e}", file=sys.stderr)
            return 1
        for item in _parse_rss_items(xml_text):
            kind = _classify(item, source)
            if not kind:
                continue
            collected.append((kind, item))

    if bootstrap:
        new_seen = seen | {it["guid"] for _, it in collected}
        save_state({"seen_guids": sorted(new_seen)})
        print(
            f"Khởi tạo state: đã ghi nhận {len(new_seen)} mục (Xcode / policy). "
            "Không tạo bài lần này. Lần chạy sau, mục mới trên RSS sẽ thành bài viết."
        )
        return 0

    CONTENT_POST.mkdir(parents=True, exist_ok=True)
    created = 0
    for kind, item in collected:
        g = item["guid"]
        if g in seen:
            continue
        folder = _post_folder_name(kind, item)
        post_dir = CONTENT_POST / folder
        if post_dir.exists():
            seen.add(g)
            continue
        post_dir.mkdir(parents=True)
        md_path = post_dir / "index.md"
        md_path.write_text(_build_markdown(kind, item), encoding="utf-8")
        seen.add(g)
        created += 1
        print(f"Tạo: {md_path.relative_to(REPO_ROOT)}")

    save_state({"seen_guids": sorted(seen)})
    if created == 0:
        print("Không có mục RSS mới.")
    else:
        print(f"Hoàn tất: {created} bài mới.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
