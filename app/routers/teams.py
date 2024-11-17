from fastapi import APIRouter, Depends
from app.models.team import Team
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_teams(db=Depends(get_db)):
    """Obtener la lista de equipos."""
    teams = db["teams"].find()  # Ejemplo con MongoDB
    return [team for team in teams]

@router.post("/")
async def create_team(team: Team, db=Depends(get_db)):
    """Crear un nuevo equipo."""
    db["team"].insert_one(team.dict())
    return {"message": "Equipo creado con éxito"}