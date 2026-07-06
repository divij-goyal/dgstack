# Skills

This directory contains the callable DG Stack skills. The installer symlinks
each listed skill into Claude Code and Codex so natural user requests can trigger
the right workflow directly.

## Installed Skills

- `tagline-generator`: taglines, headlines, slogans, positioning, YC-style
  one-liners, startup copy, and landing-page hero copy.
- `blog-writer`: blogs, essays, newsletters, LinkedIn posts, founder notes,
  product/growth articles, and explainers.
- `script-writer`: scripts, hooks, short videos, ads, UGC, dialogue, scenes,
  image prompts, and video prompts.
- `brainstorming`: startup ideas, product ideas, app ideas, creative strategy,
  dating-app conversation starters, and open-ended decisions.
- `dgstack-upgrade`: pull the latest GitHub repo and rerun setup.

## Skill Shape

Each skill owns:

- `SKILL.md`: trigger description, workflow, and output contract.
- `references/instructions.md`: deeper local technique and taste rules.
- `agents/openai.yaml`: optional short description for OpenAI/Codex surfaces.

Shared data stays outside this directory:

- `../references/principles.md`: common creative principles.
- `../brain/`: source-backed reference data and examples.

