# Tools

These scripts refresh or normalize the DG Stack brain. Run them from the repo
root unless a script says otherwise.

## Scripts

- `ingest_brain.py`: refresh YC startup data, Paul Graham essays, Lenny starter
  data, and core source READMEs.
- `ingest_yc_batch_xlsx.py`: convert a downloaded YC batch spreadsheet into a
  batch folder under `brain/sources/yc-startups/batches/`.
- `ingest_promptbazaar.py`: refresh Prompt Bazaar image/video prompt examples.
- `ingest_museon.py`: refresh Museon social/video prompt examples while
  stripping links, media URLs, creator profile data, and handles.

## Safety Checks

Run these before committing regenerated corpora:

```bash
rg -n "AIza[0-9A-Za-z_-]{20,}" . || true
python3 -m py_compile tools/*.py
find brain/sources -name '*.json' -print0 | xargs -0 -n1 jq empty
```

For prompt corpora that should not contain links:

```bash
rg -n "https?://|www\\." brain/sources/museon brain/sources/dating-openers || true
```

