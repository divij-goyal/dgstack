# Museon Prompt Brain

Video and social prompt examples extracted from Museon prompt pages.

Prompts captured: 90

## How To Use

- Use `items.jsonl` for fast search across all captured prompt examples.
- Use `prompts/<platform>-<title>-<id>.json` when a specific pattern is useful.
- Preserve the observed structure: scene, camera, action, dialogue, technical specs, negative prompts, and platform framing.
- Use engagement fields as weak signals for hooks and formats, not as guarantees of performance.
- Do not add source links, media links, creator links, or profile data to this corpus.

## Platform Counts

- instagram: 30
- sora2: 30
- tiktok: 30

## Content Type Counts

- video: 89
- carousel: 1

## Files

- `items.json`: complete normalized prompt list.
- `items.jsonl`: one prompt per line for search and retrieval.
- `prompts/`: one JSON file per prompt for targeted reading.

## Retrieval Tips

- Search by platform first: `instagram`, `tiktok`, or `sora2`.
- Search for prompt fields such as `camera`, `dialogue`, `negative_prompts`, `sceneDescription`, and `technical_specs`.
- Prefer `prompt_data` when present because it preserves the structured creative intent.
