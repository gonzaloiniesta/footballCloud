from pydantic import BaseModel
from typing import List, Optional

class Team(BaseModel):
    team_id: str
    name: str
    league: str
    country: str
    points: int
    wins : InterruptedError
    draws : int
    loses : int
    classification: int
    goals_for: int
    goals_against: int
    cards: int
    players: List[str]
    
