from pydantic import BaseModel
from typing import List, Optional

class Match(BaseModel):
    match_id: str
    home_team: str
    away_team: str
    date: str
    score: Optional[str] = None
    events: List[dict] = []
