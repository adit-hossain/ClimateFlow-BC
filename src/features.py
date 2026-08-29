"""Build leakage-aware features for next-day Squamish River streamflow."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FEATURE_PATH = PROCESSED / "hydroclimate_features.csv"


def build_features(df=None, persist=True):
    """Create predictors known by the end of each date and tomorrow's target."""
    if df is None:
        df = pd.read_csv(PROCESSED / "hydroclimate_merged.csv", parse_dates=["date"])

    required = {"date", "mean_temp_c", "precipitation_mm", "streamflow_cms"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Merged data is missing columns: {sorted(missing)}")

    features = df.copy()
    features["date"] = pd.to_datetime(features["date"], errors="coerce")
    features = features.dropna(subset=["date"]).sort_values("date")
    features = features.drop_duplicates("date", keep="first").reset_index(drop=True)

    # Fill only short internal climate gaps. Longer gaps remain missing and are
    # dropped below instead of being replaced with an unsupported value.
    climate_columns = ["mean_temp_c", "precipitation_mm"]
    features[climate_columns] = features[climate_columns].interpolate(
        method="linear", limit=3, limit_area="inside"
    )

    features["precip_lag1"] = features["precipitation_mm"].shift(1)
    features["precip_3day"] = features["precipitation_mm"].rolling(3).sum()
    features["precip_7day"] = features["precipitation_mm"].rolling(7).sum()
    features["temp_3day_mean"] = features["mean_temp_c"].rolling(3).mean()
    features["temp_7day_mean"] = features["mean_temp_c"].rolling(7).mean()
    features["streamflow_lag1"] = features["streamflow_cms"].shift(1)
    features["streamflow_lag3"] = features["streamflow_cms"].shift(3)
    # Shift first so today's flow never enters this historical rolling mean.
    features["streamflow_7day_mean"] = (
        features["streamflow_cms"].shift(1).rolling(7).mean()
    )
    features["month"] = features["date"].dt.month
    features["day_of_year"] = features["date"].dt.dayofyear
    features["target_next_day_streamflow"] = features["streamflow_cms"].shift(-1)

    # Removes the first seven history rows, the final targetless row, and any
    # observations affected by climate gaps longer than three days.
    features = features.dropna().reset_index(drop=True)

    if persist:
        PROCESSED.mkdir(parents=True, exist_ok=True)
        features.to_csv(FEATURE_PATH, index=False)

    print(f"Modeling rows: {len(features):,}")
    print(f"Date range: {features['date'].min().date()} to {features['date'].max().date()}")
    return features


if __name__ == "__main__":
    build_features()
