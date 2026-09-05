from pathlib import Path

import pandas as pd

from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    ANALYTICS_DATA_PATH
)


def test_raw_data_count():
    files = list(RAW_DATA_PATH.glob("*.json"))
    assert len(files) == 1243


def test_processed_matches():
    file_path = PROCESSED_DATA_PATH / "matches.csv"
    df = pd.read_csv(file_path)

    assert len(df) == 1243
    assert df["match_id"].nunique() == 1243


def test_processed_deliveries():
    file_path = PROCESSED_DATA_PATH / "deliveries.csv"
    df = pd.read_csv(file_path)

    assert len(df) > 0
    assert df["match_id"].nunique() == 1243


def test_player_metrics():
    file_path = (
        ANALYTICS_DATA_PATH
        / "production_player_metrics.csv"
    )

    df = pd.read_csv(file_path)

    assert len(df) > 0
    assert "player" in df.columns
    assert "overall_score" in df.columns
