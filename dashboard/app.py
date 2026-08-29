"""Streamlit dashboard for the real 2020 ClimateFlow BC analysis."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

st.set_page_config(page_title="ClimateFlow BC", page_icon="🌊", layout="wide")
st.title("ClimateFlow BC")
st.caption(
    "Real 2020 observations from Squamish Airport and Squamish River near "
    "Brackendale (Water Survey of Canada station 08GA022)"
)

feature_path = PROCESSED / "hydroclimate_features.csv"
merged_path = PROCESSED / "hydroclimate_merged.csv"
if not feature_path.exists() or not merged_path.exists():
    st.error("Required processed files are missing. Run `python src/run_all.py` first.")
    st.stop()

features = pd.read_csv(feature_path, parse_dates=["date"])
merged = pd.read_csv(merged_path, parse_dates=["date"])

# Guard against accidentally publishing stale demo outputs.
if set(merged["date"].dt.year.unique()) != {2020} or len(merged) != 366:
    st.error("Expected the verified 366-row real 2020 Squamish dataset. Re-run the real-data pipeline.")
    st.stop()

tabs = st.tabs(
    ["Overview", "Climate & Flow", "Lag Analysis", "Model Performance", "Methodology / Limitations"]
)

with tabs[0]:
    st.subheader("Study overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Daily observations", f"{len(merged):,}")
    c2.metric("Study period", "2020")
    c3.metric("Median streamflow", f"{merged['streamflow_cms'].median():.1f} m³/s")
    c4.metric("Modeling rows", f"{len(features):,}")

    wettest = merged.loc[merged["precipitation_mm"].idxmax()]
    highest_flow = merged.loc[merged["streamflow_cms"].idxmax()]
    st.markdown(
        f"""
        **Research question:** How do temperature and precipitation relate to daily streamflow,
        and how well can simple statistical and machine-learning models predict next-day streamflow?

        - Wettest day: **{wettest['date'].date()}**, {wettest['precipitation_mm']:.1f} mm precipitation,
          {wettest['streamflow_cms']:.0f} m³/s streamflow.
        - Highest-flow day: **{highest_flow['date'].date()}**, {highest_flow['streamflow_cms']:,.0f} m³/s
          streamflow and {highest_flow['precipitation_mm']:.1f} mm same-day precipitation.

        These different dates motivate lagged and rolling predictors. They do not establish causation.
        """
    )

with tabs[1]:
    st.subheader("Climate and river conditions through 2020")
    st.markdown("**Daily streamflow**")
    st.line_chart(merged.set_index("date")[["streamflow_cms"]])
    left, right = st.columns(2)
    with left:
        st.markdown("**Daily mean temperature**")
        st.line_chart(merged.set_index("date")[["mean_temp_c"]])
    with right:
        st.markdown("**Daily precipitation**")
        st.bar_chart(merged.set_index("date")[["precipitation_mm"]])
    st.caption("Missing climate observations are visible here in the merged source data.")

with tabs[2]:
    st.subheader("Lagged and rolling relationships")
    correlation_columns = [
        "streamflow_cms",
        "precipitation_mm",
        "precip_lag1",
        "precip_3day",
        "precip_7day",
        "mean_temp_c",
        "streamflow_lag1",
        "streamflow_lag3",
        "streamflow_7day_mean",
    ]
    correlations = (
        features[correlation_columns + ["target_next_day_streamflow"]]
        .corr()["target_next_day_streamflow"]
        .drop("target_next_day_streamflow")
        .sort_values(ascending=False)
        .to_frame("correlation_with_next_day_flow")
    )
    st.dataframe(correlations.round(3), width="stretch")
    st.bar_chart(correlations)
    st.info(
        "Correlation measures association, not causation. Lagged and rolling features also overlap, "
        "so their correlations should not be treated as independent effects."
    )

with tabs[3]:
    st.subheader("Held-out model performance")
    metrics_path = OUTPUTS / "metrics.json"
    if metrics_path.exists():
        model_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        rows = [
            {"Model": "Persistence Baseline", **model_metrics["persistence_baseline"]},
            {"Model": "Linear Regression", **model_metrics["linear_regression"]},
            {"Model": "Random Forest", **model_metrics["random_forest"]},
        ]
        st.dataframe(pd.DataFrame(rows).set_index("Model").round(3), width="stretch")
        st.caption(
            f"Chronological split: {model_metrics['train_start']}–{model_metrics['train_end']} train; "
            f"{model_metrics['test_start']}–{model_metrics['test_end']} test."
        )

    predictions_path = OUTPUTS / "predictions.csv"
    if predictions_path.exists():
        predictions = pd.read_csv(predictions_path, parse_dates=["date"]).set_index("date")
        plot_columns = [
            "target_next_day_streamflow",
            "linear_prediction",
            "random_forest_prediction",
        ]
        st.line_chart(predictions[plot_columns])

    importance_path = OUTPUTS / "feature_importance.csv"
    if importance_path.exists():
        st.markdown("**Random Forest feature importance**")
        importance = pd.read_csv(importance_path).head(10).set_index("feature")
        st.bar_chart(importance)
        st.caption("Feature importance is predictive, not causal, and can be shared across correlated variables.")

with tabs[4]:
    st.subheader("Methodology")
    st.markdown(
        """
        1. Clean official daily climate and hydrometric records into simple schemas.
        2. Join the datasets by date for the 2020 calendar year.
        3. Interpolate only short internal climate gaps (maximum three days).
        4. Create lagged, rolling, and seasonal features.
        5. Define tomorrow's streamflow with a one-day target shift.
        6. Train on the first 80% of dates and test on the final 20%, without shuffling.
        7. Compare persistence, Linear Regression, and Random Forest using MAE, RMSE, and R².
        """
    )
    st.subheader("Limitations")
    st.markdown(
        """
        - One year is a small sample and does not represent year-to-year climate variability.
        - The held-out period covers late autumn and winter rather than every season.
        - Squamish Airport conditions may not represent the entire river watershed.
        - Snowpack, soil moisture, elevation, and river regulation are not modeled.
        - Rare high-flow events are difficult to estimate with simple models and limited examples.
        - Linear interpolation is suitable for this retrospective study but would need a past-only alternative operationally.

        This is a learning and portfolio analysis, **not an operational flood forecasting system**.
        """
    )
