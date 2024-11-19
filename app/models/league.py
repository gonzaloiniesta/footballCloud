from pydantic import BaseModel
from typing import List, Optional, Tuple
from team import Team

class League(BaseModel):
    league_id: str
    name: str
    country: str
    classification_league: List[Team]

