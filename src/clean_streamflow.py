"""Clean real daily discharge for WSC station 08GA022."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "streamflow"
OUTPUT_PATH = ROOT / "data" / "processed" / "streamflow_clean.csv"
STATION_ID = "08GA022"


def clean_streamflow(persist=True):
    files = sorted(RAW_DIR.glob("*.csv"))
    if len(files) != 1:
        raise FileNotFoundError(f"Expected one streamflow CSV in {RAW_DIR}; found {len(files)}.")

    raw = pd.read_csv(files[0], skiprows=1, skipinitialspace=True)
    raw.columns = raw.columns.str.strip()
    required = {"ID", "PARAM", "Date", "Value"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Streamflow download is missing columns: {sorted(missing)}")

    # PARAM=1 is discharge in m³/s; PARAM=2 is water level and is out of scope.
    flow = raw.loc[(raw["ID"] == STATION_ID) & (raw["PARAM"] == 1), ["Date", "Value"]].copy()
    flow = flow.rename(columns={"Date": "date", "Value": "streamflow_cms"})
    flow["date"] = pd.to_datetime(flow["date"], errors="coerce")
    flow["streamflow_cms"] = pd.to_numeric(flow["streamflow_cms"], errors="coerce")
    flow = flow.dropna(subset=["date"]).drop_duplicates("date").sort_values("date").reset_index(drop=True)

    if persist:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        flow.to_csv(OUTPUT_PATH, index=False)

    flow_2020 = flow.loc[flow["date"].dt.year == 2020]
    if len(flow_2020) != 366 or flow_2020["streamflow_cms"].isna().any():
        raise ValueError("Expected 366 complete daily discharge observations for 2020.")

    print(f"Streamflow rows (full station record): {len(flow):,}")
    print("Verified 366 complete discharge observations for 2020.")
    return flow


if __name__ == "__main__":
    clean_streamflow()
