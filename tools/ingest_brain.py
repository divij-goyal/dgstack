#!/usr/bin/env python3
"""Build DG Stack's browsable reference brain from public source datasets."""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"
RAW = BRAIN / "raw"
SOURCES = BRAIN / "sources"
UA = "dgstack-brain-ingester/1.0 (+https://github.com/divij-goyal/dgstack)"


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:90] or "item"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = dict(attrs)
        self._href = attrs_dict.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            text = " ".join(" ".join(self._text).split())
            if text:
                self.links.append((self._href, html.unescape(text)))
            self._href = None
            self._text = []


class TextParser(HTMLParser):
    block_tags = {"p", "br", "div", "tr", "li", "h1", "h2", "h3", "blockquote"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.title = ""
        self._in_title = False
        self._skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = True
        if tag == "title":
            self._in_title = True
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = False
        if tag == "title":
            self._in_title = False
        if tag in self.block_tags:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        text = html.unescape(data).strip()
        if not text:
            return
        if self._in_title:
            self.title += text
        else:
            self.parts.append(text + " ")

    def text(self) -> str:
        text = "".join(self.parts)
        lines = [" ".join(line.split()) for line in text.splitlines()]
        lines = [line for line in lines if line]
        return "\n\n".join(lines)


def ingest_yc(homepage_limit: int) -> None:
    out = SOURCES / "yc-startups"
    raw = RAW / "yc-startups"
    data_url = "https://raw.githubusercontent.com/yc-oss/api/main/companies/all.json"
    companies = json.loads(fetch(data_url).decode("utf-8"))
    active = [c for c in companies if str(c.get("status", "")).lower() == "active"]

    write_json(raw / "all-companies.json", companies)
    write_json(out / "active-companies.json", active)

    with (out / "items.jsonl").open("w", encoding="utf-8") as f:
        for c in active:
            f.write(json.dumps({
                "type": "yc_startup",
                "name": c.get("name"),
                "one_liner": c.get("one_liner"),
                "long_description": c.get("long_description"),
                "website": c.get("website"),
                "yc_url": c.get("url"),
                "batch": c.get("batch"),
                "industry": c.get("industry"),
                "subindustry": c.get("subindustry"),
                "tags": c.get("tags"),
                "team_size": c.get("team_size"),
                "locations": c.get("all_locations"),
            }, ensure_ascii=False) + "\n")

    lines = [
        "# YC Startup Positioning Brain",
        "",
        f"Source: {data_url}",
        f"Active companies captured: {len(active)}",
        "",
        "## How To Use",
        "",
        "- For taglines, scan `active-companies.json` or `items.jsonl` for companies in the same industry.",
        "- Prefer direct customer/job/outcome language over vague category claims.",
        "- Use `homepages/` as landing-page structure references when present.",
        "",
        "## Common One-Liner Moves",
        "",
        "- `X for Y`: familiar category plus sharper audience.",
        "- `Do painful job with AI/automation`: concrete workflow, not generic transformation.",
        "- `Infrastructure layer for new behavior`: names the system role.",
        "- `Outcome in plain English`: says what the customer gets, not how the product works.",
        "",
        "## Sample Active Companies",
        "",
    ]
    for c in active[:80]:
        lines.append(f"- **{c.get('name')}**: {c.get('one_liner') or ''}")
    write_text(out / "README.md", "\n".join(lines) + "\n")

    if homepage_limit != 0:
        limit = homepage_limit if homepage_limit > 0 else len(active)
        home_dir = raw / "homepages"
        manifest = []
        for c in active[:limit]:
            website = c.get("website")
            if not website:
                continue
            try:
                body = fetch(website, timeout=5)
                filename = slugify(c.get("name", str(c.get("id")))) + ".html"
                (home_dir / filename).parent.mkdir(parents=True, exist_ok=True)
                (home_dir / filename).write_bytes(body)
                manifest.append({"name": c.get("name"), "website": website, "file": filename, "bytes": len(body)})
                time.sleep(0.15)
            except Exception as exc:
                manifest.append({"name": c.get("name"), "website": website, "error": str(exc)})
        write_json(raw / "homepage-manifest.json", manifest)


def ingest_paul_graham() -> None:
    out = SOURCES / "paul-graham"
    raw = RAW / "paul-graham"
    index_url = "https://www.paulgraham.com/articles.html"
    index_html = fetch(index_url).decode("latin-1", errors="replace")
    write_text(raw / "articles.html", index_html)
    parser = LinkParser()
    parser.feed(index_html)
    links = []
    seen = set()
    for href, title in parser.links:
        if not href.endswith(".html") or href in seen:
            continue
        seen.add(href)
        links.append({"title": title, "url": urllib.parse.urljoin(index_url, href)})

    items = []
    for essay in links:
        try:
            body = fetch(essay["url"]).decode("latin-1", errors="replace")
            raw_file = slugify(essay["title"]) + ".html"
            text_file = slugify(essay["title"]) + ".md"
            write_text(raw / "html" / raw_file, body)
            text_parser = TextParser()
            text_parser.feed(body)
            text = text_parser.text()
            write_text(out / "essays" / text_file, f"# {essay['title']}\n\nSource: {essay['url']}\n\n{text}\n")
            items.append({**essay, "raw_file": raw_file, "text_file": text_file, "word_count": len(text.split())})
            time.sleep(0.1)
        except Exception as exc:
            items.append({**essay, "error": str(exc)})

    write_json(out / "index.json", items)
    with (out / "items.jsonl").open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps({"type": "paul_graham_essay", **item}, ensure_ascii=False) + "\n")

    write_text(out / "README.md", """# Paul Graham Essay Brain

Source: https://www.paulgraham.com/articles.html

Use this corpus for founder essays, startup thinking, plain-language arguments,
and contrarian but practical blog structure.

## Style Essence

- Start with an observation that feels small but has large consequences.
- Define terms plainly, then reason from first principles.
- Prefer examples from startups, hackers, students, and investors.
- Let the argument discover its point; avoid a corporate thesis statement.
- End with a practical reframe, not a motivational slogan.

## Files

- `index.json`: essay metadata and local filenames.
- `items.jsonl`: machine-readable essay records.
- `essays/`: cleaned markdown copies for fast reading.
""")


def ingest_lenny() -> None:
    out = SOURCES / "lenny-newsletter"
    raw = RAW / "lenny-newsletter"
    base = "https://raw.githubusercontent.com/LennysNewsletter/lennys-newsletterpodcastdata/main/"
    index = json.loads(fetch(base + "index.json").decode("utf-8"))
    write_json(raw / "index.json", index)

    items = []
    selected = index.get("newsletters", []) + index.get("podcasts", [])
    for item in selected:
        filename = item["filename"]
        try:
            body = fetch(base + filename).decode("utf-8", errors="replace")
            write_text(out / filename, body)
            items.append({**item, "local_file": filename})
            time.sleep(0.05)
        except Exception as exc:
            items.append({**item, "error": str(exc)})

    write_json(out / "index.json", {"source_index": index, "items": items})
    with (out / "items.jsonl").open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps({"type": "lenny_newsletter_or_podcast", **item}, ensure_ascii=False) + "\n")

    write_text(out / "README.md", """# Lenny Newsletter Brain

Source: https://github.com/LennysNewsletter/lennys-newsletterpodcastdata

This ingests the public starter data from Lenny's official AI-friendly dataset.
The full archive requires subscriber magic-link/private-repo access from
https://lennysdata.com/.

## Style Essence

- Make the promise tactical and specific.
- Use frameworks, examples, templates, and practitioner quotes.
- Write for founders, PMs, growth leads, and operators.
- Favor useful density: takeaways, decision rules, mistakes, and examples.
- Avoid vague thought leadership; answer what the reader should do next.
""")


def ingest_static_reference_sets() -> None:
    write_text(SOURCES / "dating-openers" / "README.md", """# Dating App Conversation Starter Brain

Sources reviewed:

- https://www.reddit.com/r/Tinder/comments/10z4oa7/hit_me_with_your_best_conversation_starter/
- https://www.reddit.com/r/Tinder/comments/tbtn97/as_a_guy_is_saying_hey_hows_it_going_an_okay_way/
- https://www.reddit.com/r/Tinder/comments/8sznkh/whats_a_good_conversation_opener_to_get_girls_to/
- https://www.reddit.com/r/Tinder/comments/3ed4bl/whats_your_best_conversationstarter_for_tinder_no/

Direct Reddit JSON fetching was blocked by network security during ingestion, so
this file stores source-linked patterns rather than a scraped comment archive.

## Patterns That Tend To Get Replies

- Profile-specific question: mention one concrete photo, detail, place, hobby, or prompt.
- Compliment plus curiosity: avoid generic appearance-only compliments; ask something answerable.
- Low-pressure playful premise: an odd but easy question that invites a short answer.
- Shared-choice opener: two options that reveal taste, e.g. "chaotic road trip or perfect dinner?"
- Story prompt: ask for a tiny story, not a biography.

## Reusable Templates

- "You look genuinely happy in the [specific photo]. What was happening there?"
- "Important question: are you more [option A] or [option B]?"
- "Your [profile detail] raises a serious question: [playful specific question]?"
- "I need the backstory on [specific detail]."
- "What's the most underrated thing about [interest/place from profile]?"

## Avoid

- Copy-paste sexual lines.
- "Hey" with no context.
- Interview questions with no emotional hook.
- Overly clever openers that give the other person no easy reply path.
""")

    video_items = [
        {
            "source": "https://gist.github.com/ruvnet/e20537eb50866b2d837d4d13b066bd88",
            "pattern": "cinematic_sora",
            "essence": "Subject + environment + camera movement + lens/lighting + mood + temporal action.",
        },
        {
            "source": "https://github.com/geekjourneyx/awesome-ai-video-prompts",
            "pattern": "awesome_ai_video_prompting",
            "essence": "Prompt libraries should separate scene, motion, camera, style, audio, constraints, and negative space.",
        },
        {
            "source": "https://github.com/Eric-Lautanen/seamless-ai-video-prompt-template",
            "pattern": "continuous_shot",
            "essence": "For seamless video, define one continuous camera move, stable subject identity, and no hard cuts.",
        },
        {
            "source": "https://github.com/ai-boost/awesome-prompts/blob/main/prompts/video_gen_prompting.txt",
            "pattern": "video_generation_template",
            "essence": "Use model-aware syntax and describe physical motion, not only visual appearance.",
        },
    ]
    write_json(SOURCES / "video-prompts" / "items.json", video_items)
    write_text(SOURCES / "video-prompts" / "README.md", """# Video Prompt Brain

Use this source set for Sora, Veo, Runway, Pika, Kling, and similar text-to-video
or image-to-video prompt work.

## Core Formula

`Subject + action + environment + camera + lighting + style + timing + constraints`

## What Good Video Prompts Do

- Describe motion, not a still image.
- Control camera behavior: locked-off, dolly, orbit, handheld, macro, aerial.
- Define continuity: single shot, no cuts, same subject, stable identity.
- Specify physical details the model can render: weather, fabric, reflections, shadows.
- Keep one main action per clip unless sequencing is supported.

## Prompt Skeleton

```text
Create a [duration/style] video of [subject] doing [specific action] in
[environment]. The camera [movement/lens/framing]. Lighting is [lighting].
Mood is [emotion]. Maintain [continuity constraints]. Avoid [failure modes].
```

## Sources

See `items.json` for source URLs and extracted pattern notes.
""")


def write_brain_index() -> None:
    write_text(BRAIN / "README.md", """# DG Stack Brain

This directory is the shared reference brain for DG Stack skills. It stores raw
source artifacts, normalized item indexes, and distilled style/pattern notes.

## How Agents Should Use It

1. Start with `sources/<domain>/README.md` for the essence and usage notes.
2. Use `items.jsonl` or `index.json` for exact examples and source metadata.
3. Use `raw/` only when building landing pages, checking source context, or
   extracting additional patterns.
4. Do not copy living writers or source text verbatim. Use structure, taste,
   decision rules, and patterns.

## Source Map

- `sources/yc-startups`: startup one-liners, positioning, and homepage HTML references.
- `sources/paul-graham`: founder essay corpus and plain contrarian essay style.
- `sources/lenny-newsletter`: product/growth/operator writing examples.
- `sources/dating-openers`: dating-app conversation starter patterns.
- `sources/video-prompts`: video-generation prompt patterns and templates.

## Refresh

Run:

```bash
python3 tools/ingest_brain.py --yc-homepage-limit 100
```

Set `--yc-homepage-limit -1` to attempt every active YC homepage. That is slow
and can add many large HTML files.
""")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--yc-homepage-limit", type=int, default=100,
                        help="0 skips homepage HTML, positive limits count, -1 attempts all active YC homepages")
    args = parser.parse_args()

    write_brain_index()
    ingest_yc(args.yc_homepage_limit)
    ingest_paul_graham()
    ingest_lenny()
    ingest_static_reference_sets()


if __name__ == "__main__":
    main()
