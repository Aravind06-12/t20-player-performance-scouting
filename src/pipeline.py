from pathlib import Path

import pandas as pd

from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH
)

from src.ingestion import process_match_file


def run_pipeline():

    PROCESSED_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    json_files = sorted(
        RAW_DATA_PATH.glob("*.json")
    )

    processed_matches = []
    failures = []

    print(f"Found {len(json_files):,} JSON files")

    for file_path in json_files:

        result = process_match_file(
            file_path
        )

        if result["success"]:
            processed_matches.append(result)
        else:
            failures.append(result)

    matches_df = pd.DataFrame(
        [
            result["match_row"]
            for result in processed_matches
        ]
    )

    all_delivery_records = []

    for result in processed_matches:
        all_delivery_records.extend(
            result["delivery_records"]
        )

    deliveries_df = pd.DataFrame(
        all_delivery_records
    )

    matches_df.to_csv(
        PROCESSED_DATA_PATH / "matches.csv",
        index=False
    )

    deliveries_df.to_csv(
        PROCESSED_DATA_PATH / "deliveries.csv",
        index=False
    )

    print(f"Successful matches : {len(processed_matches):,}")
    print(f"Failed matches     : {len(failures):,}")
    print(f"Match rows         : {len(matches_df):,}")
    print(f"Delivery rows      : {len(deliveries_df):,}")

    return matches_df, deliveries_df, failures


if __name__ == "__main__":
    run_pipeline()
