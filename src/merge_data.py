"""Merge the cleaned climate and hydrometric datasets by calendar date."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_and_merge(persist=True):
    climate = pd.read_csv(PROCESSED / "climate_clean.csv", parse_dates=["date"])
    streamflow = pd.read_csv(PROCESSED / "streamflow_clean.csv", parse_dates=["date"])

    climate_columns = {"date", "mean_temp_c", "precipitation_mm"}
    streamflow_columns = {"date", "streamflow_cms"}
    if not climate_columns.issubset(climate.columns):
        raise ValueError(f"Climate file must contain {sorted(climate_columns)}")
    if not streamflow_columns.issubset(streamflow.columns):
        raise ValueError(f"Streamflow file must contain {sorted(streamflow_columns)}")

    climate = climate[list(climate_columns)].drop_duplicates("date").sort_values("date")
    streamflow = streamflow[list(streamflow_columns)].drop_duplicates("date").sort_values("date")
    merged = climate.merge(streamflow, on="date", how="inner").sort_values("date")
    merged = merged[["date", "mean_temp_c", "precipitation_mm", "streamflow_cms"]]
    merged = merged.reset_index(drop=True)

    if merged.empty:
        raise ValueError("The cleaned files have no overlapping dates.")
    if merged["streamflow_cms"].isna().any():
        raise ValueError("Merged data contains missing streamflow values.")

    if persist:
        merged.to_csv(PROCESSED / "hydroclimate_merged.csv", index=False)

    print(f"Merged rows: {len(merged):,}")
    print(f"Date range: {merged['date'].min().date()} to {merged['date'].max().date()}")
    print("Missing values:")
    print(merged.isna().sum().to_string())
    return merged


if __name__ == "__main__":
    load_and_merge()
