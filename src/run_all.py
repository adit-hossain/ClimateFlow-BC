"""Run the reusable pipeline from the existing real processed clean data."""

from features import build_features
from merge_data import load_and_merge
from train_models import train_models


def main():
    merged = load_and_merge()
    features = build_features(merged)
    train_models(features)


if __name__ == "__main__":
    main()
