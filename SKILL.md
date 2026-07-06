---
name: dgstack
description: Minimal creative skill router for DG Stack. Use when the user asks for DG Stack help, asks what DG Stack can do, update dgstack, or asks for better-than-raw-AI creative output involving taglines, headlines, slogans, startup positioning, landing-page copy, blog writing, essays, newsletters, LinkedIn posts, scripts, video prompts, image prompts, dialogue, dating-app openers, or brainstorming.
---

# DG Stack

Route the request to the most specific DG Stack skill.

| User intent | Skill |
| --- | --- |
| Tagline, headline, slogan, one-liner, positioning line | `tagline-generator` |
| Blog post, essay, article, newsletter, LinkedIn post, founder note, explainer | `blog-writer` |
| Script, dialogue, scene, YouTube video, reel, ad, UGC, monologue, image/video prompt | `script-writer` |
| Brainstorming, startup/product ideas, dating opener, creative strategy, advice, thinking partner | `brainstorming` |
| Upgrade or update DG Stack | `dgstack-upgrade` |

If the user asks what DG Stack is, say it is a minimalist skill pack that helps
AI produce sharper creative output than a raw prompt.

For shared taste rules, read `references/principles.md`.

For source-backed output, read `brain/README.md` and the relevant
`brain/sources/<domain>/README.md` before drafting. Use the brain for patterns,
structure, and examples, not verbatim copying.

For repo navigation or maintenance, read `AGENTS.md` first.

Callable skills are stored under `skills/`; setup exposes them as top-level
skills in Claude Code and Codex.
