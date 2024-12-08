from pydantic import BaseModel
from typing import List

class League(BaseModel):
    league_id: str
    name: str
    country: str
    classification_league: List[str]
