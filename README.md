# DG Stack

DG Stack is a minimalist skill pack for Claude Code and Codex. It gives your AI
assistant focused creative workflows so the output is sharper, more specific,
and less generic than a raw prompt.

Instead of asking an assistant to "write better," DG Stack gives it reusable
taste, structure, and decision rules for common creative work.

## Why Use It

General AI assistants are good at producing plausible first drafts. They are
less reliable at choosing a strong angle, avoiding generic language, and pushing
an idea until it becomes memorable.

DG Stack helps by packaging focused skills that:

- Start from the user's real goal, audience, and context
- Apply opinionated creative principles before writing
- Avoid corporate filler and obvious advice
- Produce multiple distinct directions, not tiny variations
- Rank or challenge ideas so the output is easier to act on

## Skills

| Skill | Use it for |
| --- | --- |
| `tagline-generator` | Generate, critique, and rank startup taglines, headlines, one-liners, slogans, and positioning lines. Useful when you need to explain a product clearly and memorably. |
| `blog-writer` | Plan, draft, rewrite, or improve blog posts, essays, explainers, founder notes, and thought pieces. Useful when you need the right structure, audience, and style model before writing. |
| `brainstorming` | Think through startup ideas, product ideas, creative strategy, personal decisions, learning plans, and other open-ended problems. Useful when you want a sharp thinking partner instead of a yes-man. |
| `dgstack` | Route a request to the right DG Stack skill and explain what the pack can do. |
| `dgstack-upgrade` | Update an installed DG Stack copy from GitHub and rerun setup. |

## What Makes It Different

DG Stack is intentionally small. Each skill is designed around a repeatable
workflow:

1. Understand the job to be done.
2. Read the shared DG Stack principles.
3. Apply skill-specific instructions.
4. Produce useful output with a point of view.
5. Prefer concrete, memorable, actionable work over polished filler.

The goal is not to replace your judgment. The goal is to make the assistant a
better collaborator on the first pass.

## Install

Clone the repo:

```bash
git clone https://github.com/divij-goyal/dgstack ~/.dgstack
cd ~/.dgstack
```

Install for Claude Code:

```bash
./setup --target claude
```

Install for Codex:

```bash
./setup --target codex
```

Install for both:

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
Shared taste rules live in `references/principles.md`.

## Recommended GitHub Description

```text
Creative skills for Claude Code and Codex that make AI output sharper, more specific, and less generic.
```
