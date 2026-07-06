# DG Stack Agent Guide

This repo is a creative skill pack plus a local reference brain. Start here when
an AI agent needs to understand or use the repo.

## Fast Route

1. Read `SKILL.md` to choose the right DG Stack skill.
2. Read `references/principles.md` for shared taste rules.
3. Read the selected skill's `SKILL.md`.
4. Read that skill's `references/instructions.md`.
5. If the task benefits from examples, read `brain/README.md`, then
   `brain/sources/README.md`, then the relevant source README.

## Skills

- `tagline-generator`: startup taglines, one-liners, positioning, headlines.
- `blog-writer`: blogs, essays, founder notes, explainers, product writing.
- `script-writer`: short videos, ads, dialogue, scenes, YouTube, AI video prompts.
- `brainstorming`: startup ideas, product ideas, creative strategy, decisions.
- `dgstack-upgrade`: update an installed DG Stack copy.

## Brain Layout

- `brain/README.md`: rules for using the reference brain.
- `brain/sources/README.md`: source-by-source map with retrieval paths.
- `brain/sources/<source>/README.md`: usage notes and style essence.
- `brain/sources/<source>/items.jsonl`: search-friendly normalized records.
- `brain/sources/<source>/prompts/`, `essays/`, `newsletters/`, `podcasts/`:
  targeted per-item files when a single reference is enough.
- `brain/raw/`: original or near-original artifacts used for regeneration or
  page-structure reference. Do not start here unless the source README says so.

## Editing Rules

- Keep source READMEs short and navigational. Put bulk examples in JSON/JSONL or
  per-item files.
- Do not store secrets. Redact keys in downloaded HTML or raw pages.
- For prompt corpora, do not store source links, media links, profile links, or
  creator profile data.
- Preserve generated corpora through their `tools/ingest_*.py` scripts when
  possible.
- Do not copy source prose verbatim into final user output; use structure,
  patterns, and decision rules.

