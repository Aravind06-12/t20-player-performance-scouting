import json


def load_match_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_phase(over_number):
    if over_number < 6:
        return "Powerplay"
    elif over_number < 15:
        return "Middle"
    else:
        return "Death"


def parse_match(match_data, match_id):
    info = match_data["info"]

    outcome = info.get("outcome", {})
    winner = outcome.get("winner")
    win_by = outcome.get("by", {})

    if "runs" in win_by:
        win_type = "runs"
        win_margin = win_by["runs"]
    elif "wickets" in win_by:
        win_type = "wickets"
        win_margin = win_by["wickets"]
    else:
        win_type = None
        win_margin = None

    return {
        "match_id": match_id,
        "date": info["dates"][0],
        "season": info["season"],
        "competition": info.get("event", {}).get("name"),
        "stage": info.get("event", {}).get("stage"),
        "venue": info.get("venue"),
        "city": info.get("city"),
        "team_1": info["teams"][0],
        "team_2": info["teams"][1],
        "toss_winner": info["toss"]["winner"],
        "toss_decision": info["toss"]["decision"],
        "winner": winner,
        "win_type": win_type,
        "win_margin": win_margin,
        "player_of_match": ", ".join(
            info.get("player_of_match", [])
        )
    }


def parse_deliveries(match_data, match_id):
    info = match_data["info"]
    delivery_records = []

    for innings_number, innings in enumerate(
        match_data["innings"],
        start=1
    ):
        batting_team = innings["team"]

        bowling_team = next(
            team
            for team in info["teams"]
            if team != batting_team
        )

        for over in innings["overs"]:
            for delivery in over["deliveries"]:

                extras = delivery.get("extras", {})
                wickets = delivery.get("wickets", [])

                is_wide = "wides" in extras
                is_no_ball = "noballs" in extras
                is_wicket = len(wickets) > 0

                player_out = None
                dismissal_type = None

                if wickets:
                    player_out = wickets[0]["player_out"]
                    dismissal_type = wickets[0]["kind"]

                is_legal_delivery = (
                    not is_wide
                    and not is_no_ball
                )

                runs_batter = delivery["runs"]["batter"]
                runs_extras = delivery["runs"]["extras"]
                runs_total = delivery["runs"]["total"]

                delivery_records.append({
                    "match_id": match_id,
                    "innings": innings_number,
                    "batting_team": batting_team,
                    "bowling_team": bowling_team,
                    "over": over["over"],
                    "actual_delivery": delivery["actual_delivery"],
                    "batter": delivery["batter"],
                    "non_striker": delivery["non_striker"],
                    "bowler": delivery["bowler"],
                    "runs_batter": runs_batter,
                    "runs_extras": runs_extras,
                    "runs_total": runs_total,
                    "is_wide": is_wide,
                    "is_no_ball": is_no_ball,
                    "is_legal_delivery": is_legal_delivery,
                    "is_dot_ball": (
                        runs_total == 0
                        and is_legal_delivery
                    ),
                    "is_boundary": (
                        runs_batter in [4, 6]
                    ),
                    "is_four": runs_batter == 4,
                    "is_six": runs_batter == 6,
                    "is_wicket": is_wicket,
                    "player_out": player_out,
                    "dismissal_type": dismissal_type,
                    "phase": get_phase(over["over"])
                })

    return delivery_records


def process_match_file(file_path):

    try:
        match_data = load_match_json(file_path)
        match_id = file_path.stem

        match_row = parse_match(
            match_data,
            match_id
        )

        delivery_records = parse_deliveries(
            match_data,
            match_id
        )

        return {
            "success": True,
            "file_name": file_path.name,
            "match_row": match_row,
            "delivery_records": delivery_records,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "file_name": file_path.name,
            "match_row": None,
            "delivery_records": [],
            "error": str(e)
        }
