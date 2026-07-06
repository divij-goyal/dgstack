#!/usr/bin/env python3
"""Ingest Prompt Bazaar image/video prompts into the DG Stack brain."""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"
UA = "dgstack-promptbazaar-ingester/1.0"
SITEMAP = "https://promptbazaar.byako.dev/sitemap-0.xml"
PROMPT_HOST = "https://promptbazaar.byako.dev"


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def prompt_urls_from_sitemap(sitemap_url: str) -> list[str]:
    xml = fetch_text(sitemap_url)
    root = ET.fromstring(xml)
    urls: list[str] = []
    for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        text = loc.text or ""
        if "/prompts/" in text and not text.rstrip("/").endswith("/prompts"):
            urls.append(re.sub(r"^https://promptbazaar\.pages\.dev", PROMPT_HOST, text))
    return sorted(set(urls))


def text_between(pattern: str, page: str) -> str:
    match = re.search(pattern, page, flags=re.S)
    return html.unescape(match.group(1)).strip() if match else ""


def extract_prompt(url: str) -> dict[str, object]:
    page = fetch_text(url)
    slug = slug_from_url(url)
    title = text_between(r"<h1[^>]*>\s*(.*?)\s*</h1>", page)
    description = text_between(r'<meta name="description" content="(.*?)"', page)
    crumb = text_between(r'<div class="mb-6 font-mono[^>]*>\s*(.*?)\s*</div>', page)
    category = ""
    model = ""
    if "/" in crumb:
        category, _ = [part.strip() for part in crumb.split("/", 1)]
    elif crumb:
        category = crumb.strip()
    model = text_between(
        r'<span class="font-mono text-\[10px\] text-ink-muted"[^>]*>\s*(.*?)\s*</span>\s*</div>\s*<pre',
        page,
    )

    code = text_between(r"<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>", page)
    prompt: object
    try:
        prompt = json.loads(code)
    except json.JSONDecodeError:
        prompt = code

    return {
        "slug": slug,
        "title": title,
        "description": description,
        "category": category,
        "model": model,
        "prompt": prompt,
    }


def write_outputs(records: list[dict[str, object]]) -> None:
    source_dir = BRAIN / "sources" / "promptbazaar"
    prompt_dir = source_dir / "prompts"
    source_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir.mkdir(parents=True, exist_ok=True)

    for record in records:
        (prompt_dir / f"{record['slug']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    (source_dir / "items.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (source_dir / "items.jsonl").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    category_counts: dict[str, int] = {}
    model_counts: dict[str, int] = {}
    for record in records:
        category = str(record.get("category") or "Uncategorized")
        model = str(record.get("model") or "Unknown")
        category_counts[category] = category_counts.get(category, 0) + 1
        model_counts[model] = model_counts.get(model, 0) + 1

    lines = [
        "# Prompt Bazaar Brain",
        "",
        "Image and video prompt corpus extracted from Prompt Bazaar pages.",
        "",
        f"Prompts captured: {len(records)}",
        "",
        "## How To Use",
        "",
        "- Use `items.jsonl` for fast search across all prompts.",
        "- Use `prompts/<slug>.json` when a specific prompt pattern is useful.",
        "- Preserve the structured prompt shape when generating new image/video prompts.",
        "- Adapt concepts, camera language, lighting, composition, sequencing, and negative prompts.",
        "",
        "## Category Counts",
        "",
    ]
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {category}: {count}")
    lines.extend(["", "## Model Counts", ""])
    for model, count in sorted(model_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {model}: {count}")
    lines.extend(["", "## Prompt Index", ""])
    for record in records:
        lines.append(f"- `{record['slug']}`: {record['title']} ({record.get('category')}, {record.get('model')})")

    (source_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemap", default=SITEMAP)
    args = parser.parse_args()

    urls = prompt_urls_from_sitemap(args.sitemap)
    records = [extract_prompt(url) for url in urls]
    write_outputs(records)
    print(f"Ingested {len(records)} Prompt Bazaar prompts")


if __name__ == "__main__":
    main()
