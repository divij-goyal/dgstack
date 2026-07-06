# Brain Source Index

Use this file to choose the smallest useful corpus before opening large files.

## Source Map

| Source | Use For | Start Here | Search Files |
| --- | --- | --- | --- |
| `yc-startups` | startup taglines, one-liners, positioning, landing-page references | `yc-startups/README.md` | `active-companies.json`, `items.jsonl`, `batches/*/items.jsonl` |
| `paul-graham` | founder essays, plain arguments, contrarian startup thinking | `paul-graham/README.md` | `index.json`, `items.jsonl`, `essays/*.md` |
| `lenny-newsletter` | product, growth, PM, operator writing | `lenny-newsletter/README.md` | `index.json`, `items.jsonl`, `newsletters/*.md`, `podcasts/*.md` |
| `dating-openers` | dating app opener lines and reply-friendly conversation patterns | `dating-openers/README.md` | `items.json` |
| `video-prompts` | compact video prompt formulas and reusable patterns | `video-prompts/README.md` | `items.json` |
| `promptbazaar` | structured image/video prompt examples | `promptbazaar/README.md` | `items.jsonl`, `prompts/*.json` |
| `museon` | social/video prompt examples with platform and performance metadata | `museon/README.md` | `items.jsonl`, `prompts/*.json` |

## Retrieval Order

1. Read the source README for rules, style essence, and caveats.
2. Use `items.jsonl` for broad search across a corpus.
3. Open one or a few per-item files only after narrowing the target.
4. Use `brain/raw/` only for regeneration, landing-page structure, or missing
   context that normalized files do not contain.

## Data Safety

- Do not treat raw source text as output text.
- Do not add secrets, private tokens, profile URLs, media URLs, or scraped
  account metadata to prompt corpora.
- Prefer distilled patterns and normalized records over long copied passages in
  README files.

