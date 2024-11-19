from pydantic import BaseModel
from typing import List, Optional, Tuple

class PlayerMatch(BaseModel):
    player_id: str
    goals: int
    cards: int
    min: int
    outlines: int
    tackles: int
    shots_on_target: int
    dribbles: int
    balls_lost: int
    completed_passes: int
    