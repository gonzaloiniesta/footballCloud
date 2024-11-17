from pydantic import BaseModel
from typing import List, Optional

class Player(BaseModel):
    player_id: str
    name: str
    surname: str
    team: str
    nacionality: str
    score: Optional[str] = None
    cards: int
