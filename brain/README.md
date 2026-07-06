# DG Stack Brain

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

- `sources/yc-startups`: startup one-liners, positioning, latest batch spreadsheets, and homepage HTML references.
- `sources/paul-graham`: founder essay corpus and plain contrarian essay style.
- `sources/lenny-newsletter`: product/growth/operator writing examples.
- `sources/video-prompts`: video-generation prompt patterns and templates.

## Refresh

Run:

```bash
python3 tools/ingest_brain.py --yc-homepage-limit 100
```

Set `--yc-homepage-limit -1` to attempt every active YC homepage. That is slow
and can add many large HTML files.
