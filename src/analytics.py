import pandas as pd


BOWLER_WICKET_TYPES = [
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket"
]


def build_batting_metrics(deliveries_df):

    batting = (
        deliveries_df
        .groupby("batter")
        .agg(
            runs=("runs_batter", "sum"),
            balls_faced=("is_legal_delivery", "sum"),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            dot_balls=("is_dot_ball", "sum"),
            matches=("match_id", "nunique")
        )
        .reset_index()
    )

    batting["strike_rate"] = (
        batting["runs"]
        / batting["balls_faced"]
        * 100
    )

    batting["boundaries_per_100_balls"] = (
        (batting["fours"] + batting["sixes"])
        / batting["balls_faced"]
        * 100
    )

    batting["dot_ball_rate"] = (
        batting["dot_balls"]
        / batting["balls_faced"]
        * 100
    )

    return batting


def build_bowling_metrics(deliveries_df):

    df = deliveries_df.copy()

    # Calculate bowler-conceded runs.
    # Byes and leg-byes are not charged to the bowler.
    df["bowler_runs_conceded"] = (
        df["runs_total"]
        - df.get("runs_extras", 0)
    )

    # Recalculate correctly using the raw extras information
    # when available through the original delivery columns.
    if "extras" in df.columns:

        def calculate_bowler_runs(row):
            extras = row["extras"]

            if not isinstance(extras, dict):
                extras = {}

            non_bowler_extras = (
                extras.get("byes", 0)
                + extras.get("legbyes", 0)
            )

            return (
                row["runs_total"]
                - non_bowler_extras
            )

        df["bowler_runs_conceded"] = df.apply(
            calculate_bowler_runs,
            axis=1
        )

    # Identify wickets credited to the bowler.
    df["is_bowler_wicket"] = (
        df["is_wicket"]
        & df["dismissal_type"].isin(
            BOWLER_WICKET_TYPES
        )
    )

    bowling = (
        df
        .groupby("bowler")
        .agg(
            legal_balls=("is_legal_delivery", "sum"),
            runs_conceded=(
                "bowler_runs_conceded",
                "sum"
            ),
            wickets=(
                "is_bowler_wicket",
                "sum"
            ),
            dot_balls=("is_dot_ball", "sum"),
            matches=("match_id", "nunique")
        )
        .reset_index()
    )

    bowling["economy"] = (
        bowling["runs_conceded"]
        / bowling["legal_balls"]
        * 6
    )

    bowling["wicket_rate_per_100_balls"] = (
        bowling["wickets"]
        / bowling["legal_balls"]
        * 100
    )

    bowling["dot_ball_rate"] = (
        bowling["dot_balls"]
        / bowling["legal_balls"]
        * 100
    )

    return bowling
