from typing import Optional

_last_simulation = None


def store(
    champion: str,
    top_scorer_name: str,
    top_scorer_team: str,
    top_scorer_goals: int,
    total_goals: int,
    total_matches: int,
    team_scorers: list[dict] | None = None,
):
    global _last_simulation
    _last_simulation = {
        "champion": champion,
        "top_scorer_name": top_scorer_name,
        "top_scorer_team": top_scorer_team,
        "top_scorer_goals": top_scorer_goals,
        "total_goals": total_goals,
        "total_matches": total_matches,
        "team_scorers": team_scorers or [],
    }


def retrieve() -> Optional[dict]:
    return _last_simulation


def clear():
    global _last_simulation
    _last_simulation = None
