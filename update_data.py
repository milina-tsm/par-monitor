#!/usr/bin/env python3
"""
KeHE PAR Weekly Report -> Dashboard JSON converter.

Usage:
    python update_data.py path/to/True_Sea_Moss_06_08_2026_PAR_Weekly_GREEN_SPOON_SALES.xlsx

What it does:
    1. Parses the KeHEPARDataFlowSource sheet
    2. Writes data/YYYY-MM-DD.json (week date taken from the filename, or pass --date)
    3. Updates data/manifest.json with the list of available weeks

Weekly workflow:
    1. Save the new PAR file from Green Spoon's email
    2. Run this script against it
    3. git add data/ && git commit -m "PAR week YYYY-MM-DD" && git push
    Dashboard picks the new week up automatically.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

SHEET = "KeHEPARDataFlowSource"
DATA_DIR = Path(__file__).parent / "data"

ITEM_STATUS_KEY = {
    "N": "Active",
    "T": "Temp OOS (Manufacturer)",
    "S": "Seasonal",
    "L": "Disco'd by KeHE",
    "D": "Disco'd by Supplier",
}


def parse_date_from_filename(name: str):
    m = re.search(r"(\d{2})_(\d{2})_(\d{4})", name)
    if m:
        mm, dd, yyyy = m.groups()
        return f"{yyyy}-{mm}-{dd}"
    return None


def to_date_str(val):
    if pd.isna(val):
        return None
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d")
    s = str(val).strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s or None


def num(val, default=0):
    if pd.isna(val):
        return default
    try:
        f = float(val)
        return int(f) if f == int(f) else round(f, 2)
    except (TypeError, ValueError):
        return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx", help="Path to the weekly PAR xlsx file")
    ap.add_argument("--date", help="Override week date (YYYY-MM-DD)")
    args = ap.parse_args()

    src = Path(args.xlsx)
    if not src.exists():
        sys.exit(f"File not found: {src}")

    week = args.date or parse_date_from_filename(src.name)
    if not week:
        sys.exit("Could not detect date from filename. Pass --date YYYY-MM-DD")

    df = pd.read_excel(src, sheet_name=SHEET)

    rows = []
    for _, r in df.iterrows():
        rows.append({
            "dc": num(r.get("DC")),
            "account": str(r.get("Account") or "").strip(),
            "event_type": str(r.get("Event Type") or "").strip(),
            "event_status": str(r.get("Status") or "").strip(),  # Current / Future
            "sku": str(r.get("Description") or "").strip(),
            "upc": str(r.get("UPC") or "").strip(),
            "item_status": str(r.get("Item Status") or "").strip(),
            "item_status_label": ITEM_STATUS_KEY.get(str(r.get("Item Status") or "").strip(), ""),
            "ryg": str(r.get("RYG") or "").strip(),
            "awm": num(r.get("AWM")),
            "req_dollars": num(r.get("Req $")),
            "req_qty": num(r.get("Req Qty")),
            "shipped_qty": num(r.get("Shipped Qty")),
            "est_cover": num(r.get("Est. % Cover")),
            "est_qty_short": num(r.get("Est. Qty Short")),
            "on_po": num(r.get("On PO ?")),
            "qty_oh": num(r.get("Qty OH")),
            "qty_oo": num(r.get("Qty OO")),
            "event_start": to_date_str(r.get("Event Start Dt")),
            "event_end": to_date_str(r.get("Event End Dt")),
            "po_req_by": to_date_str(r.get("PO Req By Dt (Future Events)")),
            "compliant": str(r.get("Is Compliant") or "").strip(),
            "delay_units": num(r.get("Delay Units")),
            "final_sug_ord": num(r.get("Final Sug Ord Qty")),
            "due_order": bool(r.get("Due Order")) if not pd.isna(r.get("Due Order")) else False,
            "comments": str(r.get("Comments") or "").strip(),
        })

    DATA_DIR.mkdir(exist_ok=True)
    out_file = DATA_DIR / f"{week}.json"
    out_file.write_text(json.dumps({"week": week, "source": src.name, "rows": rows},
                                   ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {out_file}  ({len(rows)} rows)")

    # Update manifest
    manifest_path = DATA_DIR / "manifest.json"
    weeks = []
    if manifest_path.exists():
        weeks = json.loads(manifest_path.read_text()).get("weeks", [])
    weeks = [w for w in weeks if w["date"] != week]
    label = datetime.strptime(week, "%Y-%m-%d").strftime("Week of %b %-d, %Y")
    weeks.append({"date": week, "file": f"{week}.json", "label": label})
    weeks.sort(key=lambda w: w["date"])
    manifest_path.write_text(json.dumps({"weeks": weeks}, indent=2))
    print(f"Manifest updated: {len(weeks)} week(s) available")


if __name__ == "__main__":
    main()
