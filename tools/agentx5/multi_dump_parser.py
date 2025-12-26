# --------------------------------------------------------------
#   multi_dump_parser.py
#   Made by Developer AI
#
#   Usage:
#       python multi_dump_parser.py dump.txt out_dir
# --------------------------------------------------------------
from __future__ import annotations
import sys
import csv
import json
import re
from pathlib import Path
from typing import Dict, List
import pandas as pd

# -----------------------------------------------------------------
# 1.  Helper: identify which "section" a header line belongs to
# -----------------------------------------------------------------
HEADER_PATTERNS: Dict[str, re.Pattern] = {
    "robinhood_sales": re.compile(
        r"ASSET NAME,RECEIVED DATE,COST BASIS\(USD\),DATE SOLD,PROCEEDS",
        re.IGNORECASE,
    ),
    "personal_finance": re.compile(
        r"Date,Original Date,Account Type,Account Name,Account Number,Institution Name",
        re.IGNORECASE,
    ),
    "crypto_movements": re.compile(
        r"Transaction,Type,Input Currency,Input Amount,Output Currency",
        re.IGNORECASE,
    ),
    "btc_daily_prices": re.compile(
        r"Start,End,Open,High,Low,Close,Volume,Market Cap",
        re.IGNORECASE,
    ),
    # Add more recognisable headers when needed
}

# Sections that should be output as JSON instead of CSV
JSON_SECTIONS = {"logic_app_json", "scriptable_js"}

# -----------------------------------------------------------------
# 2.  Streaming parser – no huge RAM spikes even on big files
# -----------------------------------------------------------------
def parse_file(in_path: Path) -> Dict[str, List[str]]:
    """
    Reads the raw dump and splits it into sections.
    Returns {section_name: [raw lines]}
    """
    sections: Dict[str, List[str]] = {}
    current_section = None

    with in_path.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            stripped = line.rstrip("\n")

            # Detect Logic-App JSON (starts with '{ "$schema":')
            if stripped.startswith('{"$schema"'):
                current_section = "logic_app_json"
                sections.setdefault(current_section, []).append(stripped)
                continue

            # Detect Scriptable JS (starts with "// Variables used by Scriptable.")
            if stripped.startswith("// Variables used by Scriptable."):
                current_section = "scriptable_js"
                sections.setdefault(current_section, []).append(stripped)
                continue

            # Detect CSV-type headers
            for name, pattern in HEADER_PATTERNS.items():
                if pattern.search(stripped):
                    current_section = name
                    sections.setdefault(current_section, []).append(stripped)
                    break
            else:
                # Normal content line → append to existing section (if any)
                if current_section:
                    sections[current_section].append(stripped)

    return sections


# -----------------------------------------------------------------
# 3.  Persist every section into its own clean file
# -----------------------------------------------------------------
def write_sections(sections: Dict[str, List[str]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, lines in sections.items():
        target = out_dir / f"{name}"
        print(f"Saving {name} → {target.with_suffix('.csv' if name not in JSON_SECTIONS else '.json')}")

        # JSON-style sections --------------------------------------
        if name in JSON_SECTIONS:
            # Join and re-format for readability
            raw_json = "\n".join(lines)
            try:
                parsed = json.loads(raw_json)
                target.with_suffix(".json").write_text(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                # Fallback: dump raw text if JSON is malformed
                target.with_suffix(".json").write_text(raw_json)
            continue

        # CSV-style sections ---------------------------------------
        header = lines[0]
        rows = lines[1:]

        # Use csv.Sniffer to auto-detect delimiter if needed
        dialect = csv.Sniffer().sniff(header)
        data = list(csv.reader([header] + rows, dialect=dialect))

        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_csv(target.with_suffix(".csv"), index=False)


# -----------------------------------------------------------------
# 4.  Example post-processing: capital-gains on Robinhood
# -----------------------------------------------------------------
def compute_capital_gains(robinhood_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(robinhood_csv, parse_dates=["RECEIVED DATE", "DATE SOLD"])
    df["gain"] = df["PROCEEDS"] - df["COST BASIS(USD)"]
    df["days_held"] = (df["DATE SOLD"] - df["RECEIVED DATE"]).dt.days
    df["long_term"] = df["days_held"] > 365
    return df


# -----------------------------------------------------------------
# 5.  CLI entry-point
# -----------------------------------------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python multi_dump_parser.py dump.txt out_dir")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])

    sections = parse_file(in_path)
    write_sections(sections, out_dir)

    # Optional: Robinhood gains summary
    robinhood_file = out_dir / "robinhood_sales.csv"
    if robinhood_file.exists():
        gains_df = compute_capital_gains(robinhood_file)
        gains_df.to_csv(out_dir / "robinhood_gains_summary.csv", index=False)
        print("Capital-gains summary written → robinhood_gains_summary.csv")


if __name__ == "__main__":
    main()
