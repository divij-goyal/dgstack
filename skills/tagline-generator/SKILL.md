---
name: tagline-generator
description: Generate, improve, critique, and rank startup taglines, headlines, slogans, one-liners, positioning lines, landing-page hero copy, YC-style company descriptions, product positioning, and concise brand messaging. Use when the user asks for taglines, headlines, slogans, one-liners, positioning, value propositions, startup copy, company descriptions, YC language, or landing-page copy.
---

# Tagline Generator

Create short, specific lines that make the company easier to understand and
remember.

## Workflow

1. Identify the product, customer, category, pain, and promised outcome.
2. Read `../../references/principles.md`.
3. Read `../../brain/sources/yc-startups/README.md`.
4. If the user asks for current or latest YC-style positioning, check
   `../../brain/sources/yc-startups/batches/` first.
5. Search `../../brain/sources/yc-startups/items.jsonl` for comparable companies,
   industries, and one-liner patterns.
6. Read `references/instructions.md`.
7. Generate distinct directions, not tiny variations.
8. Rank the best options and say why each works.

## Output

Return:

- 10 tagline/headline options
- Top 3 picks
- One-line reasoning for each top pick

If the input is vague, infer the likely positioning and keep moving.
