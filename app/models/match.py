from pydantic import Literal, BaseModel
from typing import List, Optional, Tuple
from player_match import PlayerMatch

class Match(BaseModel):
    match_id: str
    home_team: str
    away_team: str
    date: str
    score: Tuple[int, int]
    cards: Optional[Literal[0, 1, 2]] = 0
    players: List[PlayerMatch]
