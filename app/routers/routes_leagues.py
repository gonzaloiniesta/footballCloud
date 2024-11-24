from fastapi import APIRouter, Depends
from models import League
from mongodb import MongoDB

router_league = APIRouter()

def get_db():
    db = MongoDB().get_db()
    return next(db) 

@router_league.get("/")
async def get_league(db=Depends(get_db)):
    leagues = db["league"].find()
    result = []
    for league in leagues:
        league["_id"] = str(league["_id"])  # Convierte ObjectId a string
        result.append(league)
    return result
    

    
@router_league.post("/")
async def create_league(team: League):
    return {"message": "Equipo creado con éxito"}