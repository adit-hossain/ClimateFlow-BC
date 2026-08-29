import unittest

import numpy as np
import pandas as pd

from src.features import build_features
from src.train_models import metrics, train_models


class PipelineTests(unittest.TestCase):
    def test_feature_builder_creates_next_day_target_without_missing_values(self):
        dates = pd.date_range("2024-01-01", periods=30, freq="D")
        frame = pd.DataFrame({
            "date": dates,
            "mean_temp_c": np.linspace(0, 10, 30),
            "precipitation_mm": np.arange(30) % 4,
            "streamflow_cms": np.linspace(20, 50, 30),
        })
        result = build_features(frame, persist=False)
        self.assertFalse(result.isna().any().any())
        self.assertEqual(result.iloc[0]["target_next_day_streamflow"], frame.iloc[8]["streamflow_cms"])
        self.assertEqual(result.iloc[0]["streamflow_lag1"], frame.iloc[6]["streamflow_cms"])
        self.assertAlmostEqual(
            result.iloc[0]["streamflow_7day_mean"], frame.iloc[:7]["streamflow_cms"].mean()
        )
        self.assertTrue(result["date"].is_monotonic_increasing)

    def test_metrics_are_zero_for_perfect_predictions(self):
        result = metrics(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0]))
        self.assertEqual(result, {"MAE": 0.0, "RMSE": 0.0, "R2": 1.0})

    def test_modeling_split_is_chronological(self):
        dates = pd.date_range("2024-01-01", periods=80, freq="D")
        merged = pd.DataFrame({
            "date": dates,
            "mean_temp_c": np.sin(np.arange(80) / 10),
            "precipitation_mm": np.arange(80) % 5,
            "streamflow_cms": 30 + np.arange(80) * 0.5,
        })
        features = build_features(merged, persist=False)
        result, _, _ = train_models(features, persist=False)
        self.assertLess(result["train_end"], result["test_start"])
        self.assertEqual(result["train_rows"] + result["test_rows"], len(features))


if __name__ == "__main__":
    unittest.main()
