"""Clean the real 2020 Squamish Airport daily climate download."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "climate"
OUTPUT_PATH = ROOT / "data" / "processed" / "climate_clean.csv"


def clean_climate(persist=True):
    files = sorted(RAW_DIR.glob("*.csv"))
    if len(files) != 1:
        raise FileNotFoundError(f"Expected one climate CSV in {RAW_DIR}; found {len(files)}.")

    raw = pd.read_csv(files[0])
    required = ["Date/Time", "Mean Temp (°C)", "Total Precip (mm)"]
    missing = set(required) - set(raw.columns)
    if missing:
        raise ValueError(f"Climate download is missing columns: {sorted(missing)}")

    climate = raw[required].rename(
        columns={
            "Date/Time": "date",
            "Mean Temp (°C)": "mean_temp_c",
            "Total Precip (mm)": "precipitation_mm",
        }
    )
    climate["date"] = pd.to_datetime(climate["date"], errors="coerce")
    climate["mean_temp_c"] = pd.to_numeric(climate["mean_temp_c"], errors="coerce")
    climate["precipitation_mm"] = pd.to_numeric(climate["precipitation_mm"], errors="coerce")
    climate = climate.dropna(subset=["date"]).drop_duplicates("date").sort_values("date")
    climate = climate.loc[climate["date"].dt.year == 2020].reset_index(drop=True)

    if len(climate) != 366:
        raise ValueError(f"Expected 366 climate dates for leap year 2020; found {len(climate)}.")
    if persist:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        climate.to_csv(OUTPUT_PATH, index=False)

    print(f"Climate rows: {len(climate):,}")
    print(climate.isna().sum().to_string())
    return climate


if __name__ == "__main__":
    clean_climate()
