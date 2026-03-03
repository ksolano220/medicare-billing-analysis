"""
Load CMS Medicare inpatient CSV into a SQLite database.

Creates a clean schema with proper types and indexes for fast querying.
"""

import csv
import sqlite3
from pathlib import Path

CSV_PATH = Path("data/inpatient_charges.csv")
DB_PATH = Path("data/medicare.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS inpatient_charges (
    provider_id         TEXT,
    provider_name       TEXT,
    provider_street     TEXT,
    provider_city       TEXT,
    provider_state      TEXT,
    provider_state_fips TEXT,
    provider_zip        TEXT,
    provider_ruca       TEXT,
    provider_ruca_desc  TEXT,
    drg_code            TEXT,
    drg_description     TEXT,
    total_discharges    INTEGER,
    avg_covered_charges REAL,
    avg_total_payments  REAL,
    avg_medicare_payments REAL
);

CREATE INDEX IF NOT EXISTS idx_state ON inpatient_charges(provider_state);
CREATE INDEX IF NOT EXISTS idx_drg ON inpatient_charges(drg_code);
CREATE INDEX IF NOT EXISTS idx_provider ON inpatient_charges(provider_id);
"""

COLUMN_MAP = {
    "Rndrng_Prvdr_CCN": "provider_id",
    "Rndrng_Prvdr_Org_Name": "provider_name",
    "Rndrng_Prvdr_St": "provider_street",
    "Rndrng_Prvdr_City": "provider_city",
    "Rndrng_Prvdr_State_Abrvtn": "provider_state",
    "Rndrng_Prvdr_State_FIPS": "provider_state_fips",
    "Rndrng_Prvdr_Zip5": "provider_zip",
    "Rndrng_Prvdr_RUCA": "provider_ruca",
    "Rndrng_Prvdr_RUCA_Desc": "provider_ruca_desc",
    "DRG_Cd": "drg_code",
    "DRG_Desc": "drg_description",
    "Tot_Dschrgs": "total_discharges",
    "Avg_Submtd_Cvrd_Chrg": "avg_covered_charges",
    "Avg_Tot_Pymt_Amt": "avg_total_payments",
    "Avg_Mdcr_Pymt_Amt": "avg_medicare_payments",
}

NUMERIC_COLS = {"total_discharges", "avg_covered_charges", "avg_total_payments", "avg_medicare_payments"}


def clean_value(col, val):
    if col in NUMERIC_COLS:
        try:
            return float(val.replace(",", "")) if val else None
        except ValueError:
            return None
    return val.strip() if val else None


def load():
    if not CSV_PATH.exists():
        print(f"CSV not found at {CSV_PATH}. Run download_data.py first.")
        return

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA)

    print(f"Loading {CSV_PATH} into {DB_PATH}...")

    with open(CSV_PATH, "r", encoding="latin-1") as f:
        reader = csv.DictReader(f)

        rows = []
        count = 0
        for row in reader:
            mapped = {}
            for csv_col, db_col in COLUMN_MAP.items():
                mapped[db_col] = clean_value(db_col, row.get(csv_col, ""))
            rows.append(tuple(mapped[c] for c in COLUMN_MAP.values()))
            count += 1

            if len(rows) >= 10000:
                cursor.executemany(
                    f"INSERT INTO inpatient_charges VALUES ({','.join(['?'] * 15)})",
                    rows,
                )
                rows = []
                print(f"\r  Loaded {count:,} rows", end="", flush=True)

        if rows:
            cursor.executemany(
                f"INSERT INTO inpatient_charges VALUES ({','.join(['?'] * 15)})",
                rows,
            )

    conn.commit()
    print(f"\n  Total: {count:,} rows")

    # Quick validation
    result = cursor.execute("SELECT COUNT(*) FROM inpatient_charges").fetchone()
    print(f"  Verified: {result[0]:,} rows in database")

    result = cursor.execute("SELECT COUNT(DISTINCT provider_state) FROM inpatient_charges").fetchone()
    print(f"  States: {result[0]}")

    result = cursor.execute("SELECT COUNT(DISTINCT drg_code) FROM inpatient_charges").fetchone()
    print(f"  DRG codes: {result[0]}")

    conn.close()
    size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"\n  Database size: {size_mb:.1f} MB")


if __name__ == "__main__":
    load()
