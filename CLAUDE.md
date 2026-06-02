# dgstack

Divij's personal Claude Code skill pack.

## Skill routing

When user requests match a skill's purpose, invoke via the Skill tool — don't answer inline.

- User asks to upgrade dgstack, "update dgstack", "get latest dgstack" → invoke `/dgstack-upgrade`
- User asks "what skills", "list skills", "dgstack help" → invoke `/dgstack`

## Installation

```bash
git clone https://github.com/divij-goyal/dgstack ~/.claude/skills/dgstack
cd ~/.claude/skills/dgstack && ./setup
```

## Principles

- Token efficient: do more, say less
- Opinionated: one right way per task
- Personal: tuned for Divij's workflow
