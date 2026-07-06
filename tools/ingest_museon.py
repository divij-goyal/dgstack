#!/usr/bin/env python3
"""Ingest Museon prompt examples into the DG Stack brain."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"
HOST = "https://www.museon.ai"
SITEMAP = f"{HOST}/sitemap.xml"
UA = "dgstack-museon-ingester/1.0"

PROMPT_ROOTS = {
    f"{HOST}/prompts",
    f"{HOST}/prompts/tiktok",
    f"{HOST}/prompts/instagram",
    f"{HOST}/prompts/sora",
}

DROP_KEYS = {
    "avatar_url",
    "creator",
    "external_url",
    "media_url",
    "permanent_media_url",
    "permanent_thumbnail_url",
    "profile_url",
    "source_url",
    "thumbnail_url",
    "url",
}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def discover_prompt_pages(sitemap_url: str) -> list[str]:
    urls = set(PROMPT_ROOTS)
    try:
        xml = fetch_text(sitemap_url)
        root = ET.fromstring(xml)
    except Exception:
        return sorted(urls)

    for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        text = (loc.text or "").rstrip("/")
        parsed = urlparse(text)
        if parsed.netloc != "www.museon.ai":
            continue
        if not parsed.path.startswith("/prompts"):
            continue
        if parsed.path.startswith("/zh/"):
            continue
        if "/prompts/" in parsed.path and parsed.path not in {"/prompts/tiktok", "/prompts/instagram", "/prompts/sora"}:
            continue
        urls.add(text)
    return sorted(urls)


def next_flight_text(page: str) -> str:
    chunks: list[str] = []
    pattern = re.compile(r"self\.__next_f\.push\((.*?)\)</script>", re.S)
    for match in pattern.finditer(page):
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if len(payload) > 1 and isinstance(payload[1], str):
            chunks.append(payload[1])
    return "".join(chunks)


def extract_json_array(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unterminated JSON array")


def extract_prompt_arrays(page: str) -> list[list[dict[str, object]]]:
    text = next_flight_text(page)
    arrays: list[list[dict[str, object]]] = []
    cursor = 0
    marker = '"prompts":['
    while True:
        marker_index = text.find(marker, cursor)
        if marker_index == -1:
            return arrays
        array_start = text.find("[", marker_index)
        if array_start == -1:
            return arrays
        try:
            raw = extract_json_array(text, array_start)
            parsed = json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            cursor = array_start + 1
            continue
        if isinstance(parsed, list):
            arrays.append([item for item in parsed if isinstance(item, dict)])
        cursor = array_start + len(raw)


def clean_value(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: clean_value(inner)
            for key, inner in value.items()
            if key not in DROP_KEYS and not key.endswith("_url") and key != "creator"
        }
    if isinstance(value, list):
        return [clean_value(item) for item in value]
    if isinstance(value, str):
        without_urls = re.sub(r"https?://\S+|www\.\S+", "", value)
        without_handles = re.sub(r"(?<!\w)@[A-Za-z0-9_.-]+", "", without_urls)
        return re.sub(r"[ \t]+", " ", without_handles).strip()
    return value


def sanitize_prompt(record: dict[str, object]) -> dict[str, object]:
    keep_keys = [
        "content_id",
        "platform",
        "content_type",
        "title",
        "description",
        "prompt_text",
        "prompt_data",
        "duration",
        "views",
        "likes",
        "comments",
        "shares",
        "hashtags",
        "aspect_ratio",
        "created_at",
    ]
    sanitized = {
        key: clean_value(record[key])
        for key in keep_keys
        if key in record and record[key] not in (None, "", [], {})
    }
    prompt_data = sanitized.get("prompt_data")
    if isinstance(prompt_data, str):
        try:
            sanitized["prompt_data"] = clean_value(json.loads(prompt_data))
        except json.JSONDecodeError:
            pass
    return sanitized


def safe_name(record: dict[str, object]) -> str:
    platform = str(record.get("platform") or "prompt").lower()
    title = str(record.get("title") or record.get("content_id") or "item").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")[:70] or "item"
    content_id = str(record.get("content_id") or "")[:8]
    return f"{platform}-{slug}-{content_id}.json" if content_id else f"{platform}-{slug}.json"


def collect_records(urls: list[str]) -> list[dict[str, object]]:
    by_id: dict[str, dict[str, object]] = {}
    for url in urls:
        page = fetch_text(url)
        for prompts in extract_prompt_arrays(page):
            for prompt in prompts:
                sanitized = sanitize_prompt(prompt)
                content_id = str(sanitized.get("content_id") or "")
                if not content_id:
                    continue
                by_id[content_id] = sanitized
    return sorted(by_id.values(), key=lambda item: (str(item.get("platform") or ""), str(item.get("title") or "")))


def write_outputs(records: list[dict[str, object]]) -> None:
    source_dir = BRAIN / "sources" / "museon"
    prompt_dir = source_dir / "prompts"
    source_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir.mkdir(parents=True, exist_ok=True)

    for path in prompt_dir.glob("*.json"):
        path.unlink()

    for record in records:
        (prompt_dir / safe_name(record)).write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    (source_dir / "items.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (source_dir / "items.jsonl").open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    platform_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    for record in records:
        platform = str(record.get("platform") or "unknown")
        content_type = str(record.get("content_type") or "unknown")
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
        type_counts[content_type] = type_counts.get(content_type, 0) + 1

    lines = [
        "# Museon Prompt Brain",
        "",
        "Video and social prompt examples extracted from Museon prompt pages.",
        "",
        f"Prompts captured: {len(records)}",
        "",
        "## How To Use",
        "",
        "- Use `items.jsonl` for fast search across all captured prompt examples.",
        "- Use `prompts/<platform>-<title>-<id>.json` when a specific pattern is useful.",
        "- Preserve the observed structure: scene, camera, action, dialogue, technical specs, negative prompts, and platform framing.",
        "- Use engagement fields as weak signals for hooks and formats, not as guarantees of performance.",
        "- Do not add source links, media links, creator links, or profile data to this corpus.",
        "",
        "## Platform Counts",
        "",
    ]
    for platform, count in sorted(platform_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {platform}: {count}")
    lines.extend(["", "## Content Type Counts", ""])
    for content_type, count in sorted(type_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {content_type}: {count}")
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `items.json`: complete normalized prompt list.",
            "- `items.jsonl`: one prompt per line for search and retrieval.",
            "- `prompts/`: one JSON file per prompt for targeted reading.",
            "",
            "## Retrieval Tips",
            "",
            "- Search by platform first: `instagram`, `tiktok`, or `sora2`.",
            "- Search for prompt fields such as `camera`, `dialogue`, `negative_prompts`, `sceneDescription`, and `technical_specs`.",
            "- Prefer `prompt_data` when present because it preserves the structured creative intent.",
        ]
    )

    (source_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemap", default=SITEMAP)
    parser.add_argument("--page", action="append", dest="pages")
    args = parser.parse_args()

    urls = sorted(set(args.pages or discover_prompt_pages(args.sitemap)))
    records = collect_records(urls)
    write_outputs(records)
    print(f"Ingested {len(records)} Museon prompts from {len(urls)} pages")


if __name__ == "__main__":
    main()
