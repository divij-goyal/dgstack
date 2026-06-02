---
name: dgstack
version: 0.1.0
description: Divij's personal Claude Code skill pack — opinionated tools for shipping fast.
triggers:
  - dgstack help
  - list dgstack skills
  - what skills do you have
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# dgstack

Personal skill pack by Divij Goyal. Run `/dgstack-upgrade` to update.

## Skills

| Command | Purpose |
|---------|---------|
| `/dgstack` | List skills / help |
| `/dgstack-upgrade` | Upgrade dgstack to latest |
| `/catalyst` | Find small-cap stocks with one pending catalyst (FDA, DoD contract, etc.) |

## Routing

When the user asks "what can you do", "list skills", or "dgstack help", show the table above.
