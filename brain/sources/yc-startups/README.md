# YC Startup Positioning Brain

Source: https://raw.githubusercontent.com/yc-oss/api/main/companies/all.json
Active companies captured: 4144

## How To Use

- If a relevant latest-batch folder exists under `batches/`, start there before
  using the broader all-YC corpus.
- For taglines, scan `active-companies.json` or `items.jsonl` for companies in the same industry.
- Prefer direct customer/job/outcome language over vague category claims.
- Use `homepages/` as landing-page structure references when present.

## Latest Batch Data

- `batches/p26-demo-day/`: P26 Demo Day spreadsheet with company names,
  websites, one-liners, categories, markets, and presentation order.

## Common One-Liner Moves

- `X for Y`: familiar category plus sharper audience.
- `Do painful job with AI/automation`: concrete workflow, not generic transformation.
- `Infrastructure layer for new behavior`: names the system role.
- `Outcome in plain English`: says what the customer gets, not how the product works.

## Files

- `active-companies.json`: complete active-company records.
- `items.jsonl`: one active company per line for search and retrieval.
- `batches/<batch>/`: latest-batch datasets when available.
- `homepages/`: downloaded homepage HTML references when generated.

## Retrieval Tips

- Search by industry, customer type, market, or problem phrase before drafting.
- For latest YC-style language, inspect `batches/p26-demo-day/items.jsonl` first.
- For landing-page structure, use homepage HTML only as layout reference and
  redact any discovered secrets before committing.
