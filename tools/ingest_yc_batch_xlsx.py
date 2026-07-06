#!/usr/bin/env python3
"""Ingest a YC demo day company spreadsheet into the DG Stack brain."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"
NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "yc-batch"


def cell_text(cell: ET.Element) -> str:
    inline = cell.find("x:is", NS)
    if inline is not None:
        return "".join(t.text or "" for t in inline.findall(".//x:t", NS)).strip()
    value = cell.find("x:v", NS)
    return (value.text or "").strip() if value is not None else ""


def read_xlsx_rows(path: Path) -> list[list[str]]:
    with ZipFile(path) as archive:
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    rows: list[list[str]] = []
    for row in sheet.findall(".//x:sheetData/x:row", NS):
        values = [cell_text(cell) for cell in row.findall("x:c", NS)]
        if any(values):
            rows.append(values)
    return rows


def normalize_rows(rows: list[list[str]]) -> list[dict[str, object]]:
    headers = rows[0]
    records = []
    for raw in rows[1:]:
        padded = raw + [""] * (len(headers) - len(raw))
        row = dict(zip(headers, padded))
        records.append({
            "type": "yc_demo_day_company",
            "batch": "P26",
            "name": row.get("Name", ""),
            "website": row.get("Website", ""),
            "one_liner": row.get("Description", ""),
            "demo_day_url": row.get("Slide and Contact Information", ""),
            "presentation_day": int(row["Presentation Day"]) if row.get("Presentation Day") else None,
            "presentation_order": int(row["Presentation Day Order"]) if row.get("Presentation Day Order") else None,
            "categories": [x.strip() for x in row.get("Categories", "").split(",") if x.strip()],
            "markets": [x.strip() for x in row.get("Markets", "").split(",") if x.strip()],
            "off_the_record": bool(row.get("Off The Record?")),
            "non_profit": bool(row.get("Non-Profit?")),
        })
    return records


def write_outputs(input_path: Path, batch: str, records: list[dict[str, object]]) -> None:
    slug = slugify(f"{batch}-demo-day")
    source_dir = BRAIN / "sources" / "yc-startups" / "batches" / slug
    raw_dir = BRAIN / "raw" / "yc-startups" / "batches" / slug
    source_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(input_path, raw_dir / input_path.name)

    (source_dir / "companies.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (source_dir / "items.jsonl").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    categories: dict[str, int] = {}
    markets: dict[str, int] = {}
    for record in records:
        for category in record["categories"]:
            categories[category] = categories.get(category, 0) + 1
        for market in record["markets"]:
            markets[market] = markets.get(market, 0) + 1

    lines = [
        f"# {batch} Demo Day Company Brain",
        "",
        f"Raw source: `brain/raw/yc-startups/batches/{slug}/{input_path.name}`",
        f"Companies captured: {len(records)}",
        "",
        "## How To Use",
        "",
        "- Use this batch before the older all-YC corpus when the user asks for latest YC-style taglines.",
        "- Compare companies by `categories` and `markets` before drafting positioning.",
        "- Use `one_liner` as reference material for compression patterns, not text to copy.",
        "",
        "## Category Counts",
        "",
    ]
    for category, count in sorted(categories.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {category}: {count}")
    lines.extend(["", "## Market Counts", ""])
    for market, count in sorted(markets.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {market}: {count}")
    lines.extend(["", "## Sample Lines", ""])
    for record in records[:40]:
        lines.append(f"- **{record['name']}**: {record['one_liner']}")
    (source_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--batch", default="P26")
    args = parser.parse_args()

    rows = read_xlsx_rows(args.xlsx)
    records = normalize_rows(rows)
    for record in records:
        record["batch"] = args.batch
    write_outputs(args.xlsx, args.batch, records)
    print(f"Ingested {len(records)} companies from {args.xlsx}")


if __name__ == "__main__":
    main()
