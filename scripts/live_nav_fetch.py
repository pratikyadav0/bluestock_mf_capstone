"""
Bluestock MF Capstone — Live NAV Fetcher

Fetches the latest NAV from https://api.mfapi.in/mf/{code} for 5 bluechip
schemes and saves individual CSVs into data/raw/.
"""

from pathlib import Path
import json
import requests
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# 5 target schemes
SCHEMES = {
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_Large_Cap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}

API_URL = "https://api.mfapi.in/mf/{code}"


def fetch_live_nav(code: int, label: str) -> pd.DataFrame | None:
    """Fetch NAV data for a single scheme from mfapi.in."""
    url = API_URL.format(code=code)
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        print(f"    ✗  Failed to fetch {label} ({code}): {e}")
        return None

    data = payload.get("data", [])
    if not data:
        print(f"    ⚠  No data returned for {label}")
        return None

    df = pd.DataFrame(data)
    # API returns {"date": "DD-MM-YYYY", "nav": "123.456"}
    df.rename(columns={"nav": "nav"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df["amfi_code"] = code
    df = df[["amfi_code", "date", "nav"]].dropna()
    df.sort_values("date", inplace=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df


def run_live_fetch() -> None:
    """Fetch live NAV for all target schemes and save to CSVs."""
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║             BLUESTOCK MF — LIVE NAV FETCHER                        ║")
    print("╚══════════════════════════════════════════════════════════════════════╝\n")

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for code, label in SCHEMES.items():
        print(f"  ▸ Fetching {label} (AMFI {code}) …")
        df = fetch_live_nav(code, label)
        if df is not None:
            outpath = RAW_DIR / f"live_nav_{label}.csv"
            df.to_csv(outpath, index=False)
            print(f"    → saved {outpath.name}  ({len(df):,} rows, latest NAV = {df['nav'].iloc[-1]})")

    print("\n  ✓  Live NAV fetch complete\n")


if __name__ == "__main__":
    run_live_fetch()
