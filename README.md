# DG Stack

DG Stack is a minimalist skill pack for making AI output less generic.

The MVP focuses on three high-value creative workflows:

| Skill | Use it for |
| --- | --- |
| `tagline-generator` | Startup taglines, headlines, one-liners, positioning lines |
| `blog-writer` | Blog posts, essays, explainers, founder notes |
| `brainstorming` | Creative thinking with a strong point of view |

The goal is simple: produce output that feels 50x better than a raw prompt to a
general AI assistant.

## Install

```bash
git clone https://github.com/divij-goyal/dgstack ~/.dgstack
cd ~/.dgstack
./setup --target claude
```

For Codex:

```bash
./setup --target codex
```

For both:

```bash
./setup --target both
```

Restart the agent app after setup.

## Structure

```text
dgstack/
├── SKILL.md
├── references/principles.md
├── tagline-generator/
├── blog-writer/
├── brainstorming/
├── dgstack-upgrade/
└── setup
```

Each sub-skill keeps its detailed instructions in `references/instructions.md`.
That is where the next step should add the actual DG frameworks and examples.
