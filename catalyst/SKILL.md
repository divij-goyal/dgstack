---
name: catalyst
version: 0.1.0
description: Find small/micro-cap stocks with one pending catalyst that could revalue the company — FDA approvals, defense contracts, Phase 3 readouts, permit grants, earnings inflections.
triggers:
  - find catalyst stocks
  - scan for catalyst
  - what stocks could pop
  - healthcare catalyst
  - defense catalyst
  - small cap catalyst
  - find stocks with pending catalysts
  - evaluate stocks
  - stock catalyst scan
allowed-tools:
  - WebSearch
  - WebFetch
  - Bash
  - Write
  - Read
---

# /catalyst

Find small/micro-cap stocks with ONE pending catalyst that could revalue the company.

## Philosophy

A catalyst stock has:
- **Small float** — market cap $10M–$500M (the move has room)
- **Clear binary event** — one specific pending thing that changes the trajectory
- **Asymmetric upside** — if the catalyst hits, the market cap re-rates 2x–10x+
- **Defined timeline** — not "someday", but a dateable window

Sectors with repeatable catalyst patterns:
| Sector | Catalyst type |
|--------|--------------|
| Biotech/Healthcare | FDA PDUFA date, Phase 3 readout, NDA submission |
| Defense | DoD contract award, RFP selection, NDAA authorization |
| Mining/Energy | Permit approval, resource upgrade, offtake agreement |
| Tech (small) | Major partnership, DoD/SBIR award, customer concentration win |
| Financials | Regulatory approval (charter, license), M&A target |

---

## Workflow

### Step 0: Parse intent

Check if the user specified:
- A **sector** (healthcare, defense, biotech, energy, mining, tech)
- A **market cap range** (default: $10M–$500M)
- A **timeline** (default: catalysts expected within 6 months)
- A **keyword** (e.g. "FDA approval", "DoD contract", "Phase 3")

If nothing specified, run a broad scan across biotech + defense (highest hit rate for this pattern).

### Step 1: Find candidates

Run 2–3 targeted web searches to surface stocks with the catalyst pattern. Use specific queries:

**For biotech/healthcare:**
```
WebSearch: "PDUFA date 2025" small cap biotech pending FDA approval site:biopharmcatalyst.com OR site:seeking alpha
WebSearch: "FDA approval catalyst" "$50 million market cap" OR "$100 million market cap" 2025
WebSearch: small cap biotech "phase 3 results" expected 2025 catalyst
```

**For defense:**
```
WebSearch: small cap defense stock "contract award" pending 2025 "$100 million market cap"
WebSearch: "DoD contract" pending award small cap defense 2025 catalyst
WebSearch: defense "IDIQ" OR "LPTA" award expected 2025 micro cap
```

**For mining/energy:**
```
WebSearch: small cap mining "permit approval" pending 2025 catalyst
WebSearch: micro cap energy "offtake agreement" pending 2025
```

**For broad scan:**
```
WebSearch: small cap stocks "pending catalyst" 2025 market cap under 500 million
WebSearch: micro cap "binary event" 2025 FDA OR contract OR approval
```

Pull 5–8 candidate tickers from the results.

### Step 2: Evaluate each candidate

For each ticker, gather:

```
WebSearch: [TICKER] stock market cap price catalyst 2025
WebSearch: [TICKER] pending [catalyst-type] timeline
WebFetch: https://finance.yahoo.com/quote/[TICKER]  (price, market cap, 52w range)
WebSearch: [TICKER] SEC filing OR investor presentation catalyst date
```

Extract:
- **Current price** and **market cap**
- **The ONE catalyst**: what exactly is pending, what is the specific event
- **Timeline**: when is it expected (PDUFA date, contract decision deadline, etc.)
- **What happens if it hits**: comparable company re-rating, analyst targets, historical analogues
- **What happens if it misses**: downside floor (cash position, other assets)
- **Risk/reward ratio**: upside % / downside %

### Step 3: Score each stock

Score 1–5 on each dimension (5 = best):

| Dimension | What to look for |
|-----------|-----------------|
| **Catalyst clarity** | Is the event specific and dateable? (5 = exact date known) |
| **Catalyst size** | How much does market cap change if it hits? (5 = 3x+) |
| **Downside floor** | Cash runway, book value, alternative value (5 = limited downside) |
| **Timeline** | How soon? (5 = within 3 months) |
| **Market awareness** | Is it under the radar? (5 = low institutional coverage) |

Total score out of 25. Rank candidates.

### Step 4: Output report

Print a clean report:

```
─────────────────────────────────────────────
CATALYST SCAN — [Sector] — [Date]
─────────────────────────────────────────────

#1  [TICKER] — [Company Name]
    Price: $X.XX | Mkt Cap: $XXM | 52w: $X–$X
    
    THE CATALYST: [One sentence — what is pending]
    Timeline: [Month Year or "Q3 2025"]
    
    Bull case: [What happens if catalyst hits — comparable, %, analyst target]
    Bear case: [What happens if it misses — floor, cash position]
    Risk/reward: [X:1]
    
    Score: [XX/25] — Catalyst: X | Size: X | Floor: X | Timeline: X | Awareness: X
    
    Why now: [1–2 sentences on why this is the moment]

─────────────────────────────────────────────
#2  [TICKER] ...
```

Show top 3–5 stocks only. Quality over quantity.

### Step 5: Disclaimer

Always append:
```
⚠ This is not financial advice. Do your own due diligence before trading.
  Small/micro-cap stocks are volatile and illiquid. Catalysts can miss.
```

---

## Quick mode

If the user says "quick catalyst scan" or "just give me one", return only the #1 pick with full detail. Skip the ranked list.

## Save mode

If the user says "save this" or "save the scan", write the report to `catalyst-scan-[YYYYMMDD].md` in the current directory.

## Follow-up

After the report, offer:
- "Deep dive on [TICKER]?" — runs a more detailed analysis on one stock
- "Watch list?" — adds tickers to a `watchlist.md` in the current directory
