# DG Stack

DG Stack is a minimalist creative skill pack.

Start with `AGENTS.md` for repo navigation. It is the canonical AI-facing map
for skills, brain sources, and editing rules.

Callable skills live under `skills/`. The root `SKILL.md` is only the router
and repo-level install/update anchor.

## Routing

- Taglines, headlines, slogans, one-liners -> `tagline-generator`
- Blog posts, essays, articles, founder notes -> `blog-writer`
- Scripts, dialogue, scenes, YouTube videos, reels, ads -> `script-writer`
- Brainstorming, idea sharpening, advice, creative strategy -> `brainstorming`
- DG Stack help or skill list -> `dgstack`
- DG Stack update requests -> `dgstack-upgrade`

For source-backed work, read `brain/README.md` and the relevant
`brain/sources/<domain>/README.md` before drafting. Use source data as
reference material and style/pattern guidance, not as text to copy.

## Install

```bash
./setup --target claude
./setup --target codex
./setup --target both
```
