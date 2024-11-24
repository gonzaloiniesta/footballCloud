from fastapi import APIRouter, Depends
from models import Player
from mongodb import MongoDB

router_player = APIRouter()

def get_db():
    db = MongoDB().get_db()
    return next(db) 

@router_player.get("/")
async def get_league(db=Depends(get_db)):
    players = db["players"].find()
    result = []
    for player in players:
        player["_id"] = str(player["_id"])  # Convierte ObjectId a string
        result.append(player)
    return result

@router_player.post("/")
async def create_team(team: Player):
    return {"message": "Equipo creado con éxito"}