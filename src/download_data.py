"""
Download Medicare Inpatient Hospitals data from CMS.

Source: Centers for Medicare & Medicaid Services
Dataset: Medicare Inpatient Hospitals - by Provider and Service (FY2022)
"""

import ssl
import os
from urllib.request import urlopen, Request
from pathlib import Path

DATA_URL = (
    "https://data.cms.gov/sites/default/files/2024-05/"
    "7d1f4bcd-7dd9-4fd1-aa7f-91cd69e452d3/"
    "MUP_INP_RY24_P03_V10_DY22_PrvSvc.CSV"
)

OUTPUT_PATH = Path("data/inpatient_charges.csv")


def download():
    if OUTPUT_PATH.exists():
        size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
        print(f"Data already exists ({size_mb:.1f} MB): {OUTPUT_PATH}")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Downloading CMS Medicare Inpatient data...")
    print(f"Source: {DATA_URL}")

    req = Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, context=ctx) as response:
        total = response.headers.get("Content-Length")
        total = int(total) if total else None

        downloaded = 0
        with open(OUTPUT_PATH, "wb") as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r  {downloaded / 1e6:.1f} / {total / 1e6:.1f} MB ({pct:.0f}%)", end="", flush=True)
                else:
                    print(f"\r  {downloaded / 1e6:.1f} MB", end="", flush=True)

    print()
    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Saved to {OUTPUT_PATH} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    download()
