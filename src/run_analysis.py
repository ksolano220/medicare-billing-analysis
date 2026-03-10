"""
Run all SQL queries against the Medicare database and save results.

Executes each .sql file in the queries/ directory, prints a summary,
and saves full results as CSVs in outputs/.
"""

import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("data/medicare.db")
QUERIES_DIR = Path("queries")
OUTPUT_DIR = Path("outputs")


def run_query(conn, sql_path):
    sql = sql_path.read_text()
    cursor = conn.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return columns, rows


def save_csv(columns, rows, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)


def print_table(columns, rows, max_rows=10):
    # Calculate column widths
    widths = [len(c) for c in columns]
    display_rows = rows[:max_rows]
    for row in display_rows:
        for i, val in enumerate(row):
            formatted = f"{val:,.2f}" if isinstance(val, float) else str(val or "")
            widths[i] = max(widths[i], len(formatted))

    # Header
    header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(columns))
    print(f"  {header}")
    print(f"  {'-' * len(header)}")

    # Rows
    for row in display_rows:
        formatted = []
        for i, val in enumerate(row):
            if isinstance(val, float):
                formatted.append(f"{val:,.2f}".ljust(widths[i]))
            else:
                formatted.append(str(val or "").ljust(widths[i]))
        print(f"  {' | '.join(formatted)}")

    if len(rows) > max_rows:
        print(f"  ... and {len(rows) - max_rows} more rows (see CSV)")


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run load_db.py first.")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    query_files = sorted(QUERIES_DIR.glob("*.sql"))
    print(f"Running {len(query_files)} queries against {DB_PATH}\n")

    for sql_path in query_files:
        name = sql_path.stem
        print(f"{'=' * 60}")
        print(f"  {name.replace('_', ' ').upper()}")
        print(f"{'=' * 60}")

        try:
            columns, rows = run_query(conn, sql_path)

            # Save full results
            output_path = OUTPUT_DIR / f"{name}.csv"
            save_csv(columns, rows, output_path)

            # Print preview
            print(f"  Results: {len(rows)} rows\n")
            print_table(columns, rows)
            print(f"\n  Saved: {output_path}\n")

        except Exception as e:
            print(f"  ERROR: {e}\n")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
