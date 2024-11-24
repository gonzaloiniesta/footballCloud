from fastapi import APIRouter, Depends
from models import Match
from mongodb import MongoDB

router_match = APIRouter()

def get_db():
    db = MongoDB().get_db()
    return next(db) 

@router_match.get("/")
async def get_league(db=Depends(get_db)):
    matches = db["matches"].find()
    result = []
    for match in matches:
        match["_id"] = str(match["_id"])  # Convierte ObjectId a string
        result.append(match)
    return result
    


@router_match.post("/")
async def create_team(team: Match):
    return {"message": "Equipo creado con éxito"}