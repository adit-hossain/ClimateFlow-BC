"""Train and evaluate simple next-day streamflow models chronologically."""

import json
from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
MODELS = OUTPUTS / "models"

# Every predictor is known by the end of the date on which the forecast is made.
# Including today's flow makes comparison with the persistence baseline fair.
FEATURES = [
    "streamflow_cms",
    "mean_temp_c",
    "precipitation_mm",
    "precip_lag1",
    "precip_3day",
    "precip_7day",
    "temp_3day_mean",
    "temp_7day_mean",
    "streamflow_lag1",
    "streamflow_lag3",
    "streamflow_7day_mean",
    "month",
    "day_of_year",
]
TARGET = "target_next_day_streamflow"


def calculate_metrics(actual, predicted):
    """Return standard regression metrics as JSON-safe floats."""
    return {
        "MAE": float(mean_absolute_error(actual, predicted)),
        "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
        "R2": float(r2_score(actual, predicted)),
    }


metrics = calculate_metrics


def train_models(df=None, persist=True):
    """Fit on the first 80% of dates and evaluate on the final 20%."""
    if df is None:
        df = pd.read_csv(PROCESSED / "hydroclimate_features.csv", parse_dates=["date"])

    required = set(FEATURES + [TARGET, "date"])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Feature data is missing columns: {sorted(missing)}")

    df = df.sort_values("date").reset_index(drop=True)
    if len(df) < 20:
        raise ValueError("At least 20 complete rows are required for modeling.")

    split_index = int(len(df) * 0.80)
    train = df.iloc[:split_index].copy()
    test = df.iloc[split_index:].copy()
    if train["date"].max() >= test["date"].min():
        raise ValueError("Chronological split failed: training and test dates overlap.")

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test, y_test = test[FEATURES], test[TARGET]

    baseline_predictions = test["streamflow_cms"].to_numpy()
    linear_model = LinearRegression().fit(X_train, y_train)
    linear_predictions = linear_model.predict(X_test)
    random_forest = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    ).fit(X_train, y_train)
    forest_predictions = random_forest.predict(X_test)

    model_metrics = {
        "dataset": "Real 2020 Squamish climate and streamflow data",
        "modeling_rows": len(df),
        "train_rows": len(train),
        "test_rows": len(test),
        "train_start": str(train["date"].min().date()),
        "train_end": str(train["date"].max().date()),
        "test_start": str(test["date"].min().date()),
        "test_end": str(test["date"].max().date()),
        "persistence_baseline": calculate_metrics(y_test, baseline_predictions),
        "linear_regression": calculate_metrics(y_test, linear_predictions),
        "random_forest": calculate_metrics(y_test, forest_predictions),
    }

    predictions = test[["date", "streamflow_cms", TARGET]].copy()
    predictions["baseline_prediction"] = baseline_predictions
    predictions["linear_prediction"] = linear_predictions
    predictions["random_forest_prediction"] = forest_predictions

    importance = pd.DataFrame(
        {"feature": FEATURES, "importance": random_forest.feature_importances_}
    ).sort_values("importance", ascending=False)

    comparison = pd.DataFrame(
        [
            {"model": "Persistence Baseline", **model_metrics["persistence_baseline"]},
            {"model": "Linear Regression", **model_metrics["linear_regression"]},
            {"model": "Random Forest", **model_metrics["random_forest"]},
        ]
    )

    if persist:
        FIGURES.mkdir(parents=True, exist_ok=True)
        MODELS.mkdir(parents=True, exist_ok=True)
        (OUTPUTS / "metrics.json").write_text(
            json.dumps(model_metrics, indent=2), encoding="utf-8"
        )
        predictions.to_csv(OUTPUTS / "predictions.csv", index=False)
        importance.to_csv(OUTPUTS / "feature_importance.csv", index=False)
        comparison.to_csv(OUTPUTS / "model_comparison.csv", index=False)
        joblib.dump(linear_model, MODELS / "linear_regression.joblib")
        joblib.dump(random_forest, MODELS / "random_forest.joblib")

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(predictions["date"], predictions[TARGET], label="Actual", linewidth=2)
        ax.plot(predictions["date"], linear_predictions, label="Linear Regression")
        ax.plot(predictions["date"], forest_predictions, label="Random Forest")
        ax.set(title="Next-Day Streamflow: Actual vs Predicted", ylabel="Streamflow (m³/s)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIGURES / "actual_vs_predicted.png", dpi=160)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 5))
        top = importance.head(10).sort_values("importance")
        ax.barh(top["feature"], top["importance"], color="#2a9d8f")
        ax.set(title="Random Forest Feature Importance", xlabel="Importance")
        fig.tight_layout()
        fig.savefig(FIGURES / "feature_importance.png", dpi=160)
        plt.close(fig)

    print(comparison.round(3).to_string(index=False))
    return model_metrics, predictions, importance


def train():
    """Compatibility wrapper for the original entry point."""
    return train_models()[0]


if __name__ == "__main__":
    train_models()
