# dgstack

Divij's personal Claude Code skill pack.

## Install

```bash
git clone https://github.com/divij-goyal/dgstack ~/.claude/skills/dgstack
cd ~/.claude/skills/dgstack && ./setup
```

Restart Claude Code. Skills are now available.

## Update

Say `upgrade dgstack` or run:

```bash
cd ~/.claude/skills/dgstack && git pull && ./setup
```

## Skills

| Skill | Trigger |
|-------|---------|
| `/dgstack` | `dgstack help`, `list skills` |
| `/dgstack-upgrade` | `upgrade dgstack` |

## Adding a skill

1. `mkdir my-skill && cat > my-skill/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: my-skill
   version: 0.1.0
   description: What it does.
   triggers:
     - phrase that invokes it
   allowed-tools:
     - Bash
     - Read
   ---
   ```
2. Run `./setup` — it auto-discovers any directory containing `SKILL.md`
