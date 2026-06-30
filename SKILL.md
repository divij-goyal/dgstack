---
name: dgstack
description: Minimal creative skill router for DG Stack. Use when the user asks for DG Stack help, asks what DG Stack can do, or asks for better-than-raw-AI creative output involving taglines, headlines, blog writing, or brainstorming.
---

# DG Stack

Route the request to the most specific DG Stack skill.

| User intent | Skill |
| --- | --- |
| Tagline, headline, slogan, one-liner, positioning line | `tagline-generator` |
| Blog post, essay, article, founder note, explainer | `blog-writer` |
| Brainstorming, idea sharpening, creative strategy, advice, thinking partner | `brainstorming` |
| Upgrade or update DG Stack | `dgstack-upgrade` |

If the user asks what DG Stack is, say it is a minimalist skill pack that helps
AI produce sharper creative output than a raw prompt.

For shared taste rules, read `references/principles.md`.
