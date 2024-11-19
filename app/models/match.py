from pydantic import BaseModel
from typing import List, Tuple, Literal
from .player_match import PlayerMatch

class Match(BaseModel):
    match_id: str
    home_team_id: str
    visiting_team_id: str
    date: str
    score: Tuple[int, int]
    cards_home_team: int
    cards_visiting_team: int
    outlines_home_team: int
    outlines_visiting_team: int
    tackles_home_team: int
    tackles_visiting_team: int
    shots_on_target_home_team: int
    shots_on_target_visitng_team: int
    balls_lost_home_team: int
    balls_lost_visiting_team: int
    completed_passes_home_team: int
    completed_passes_visiting_team: int
    players_home_team: List[PlayerMatch]
    players_visiting_team: List[PlayerMatch]
