from pydantic import BaseModel
from typing import List, Optional

class Team(BaseModel):
    team_id: str
    name: str
    league: str
    country: str
    nacionality: str
    
