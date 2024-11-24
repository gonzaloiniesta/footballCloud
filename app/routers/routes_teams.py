from fastapi import APIRouter, Depends
from models import Team
from mongodb import MongoDB

router_team = APIRouter()

def get_db():
    db = MongoDB().get_db()
    return next(db) 

@router_team.get("/")
async def get_league(db=Depends(get_db)):
    teams = db["teams"].find()
    result = []
    for team in teams:
        team["_id"] = str(team["_id"])  # Convierte ObjectId a string
        result.append(team)
    return result

@router_team.post("/")
async def create_team(team: Team):
    return {"message": "Equipo creado con éxito"}