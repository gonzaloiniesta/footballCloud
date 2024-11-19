from pydantic import BaseModel

class PlayerMatch(BaseModel):
    player_id: str
    goals: int
    cards: int
    minutes: int
    outlines: int
    tackles: int
    shots_on_target: int
    dribbles: int
    balls_lost: int
    completed_passes: int
    