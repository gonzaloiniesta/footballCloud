from pydantic import BaseModel

class Player(BaseModel):
    player_id: str
    name: str
    surname: str
    nacionality: str
    team_id: str
    total_goals: int
    total_cards: int
    total_minutes: int
    total_outlines: int
    total_tackles: int
    total_shots_on_target: int
    total_dribbles: int
    total_balls_lost: int
    total_completed_passes: int
