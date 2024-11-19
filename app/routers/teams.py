from fastapi import APIRouter, Depends
from models import Team
from mongodb import MongoDB

router = APIRouter()

@router.get("/")
async def get_teams(db=Depends(MongoDB.get_db())):
    """Obtener la lista de equipos."""
    teams = db["teams"].find()  # Ejemplo con MongoDB
    return [team for team in teams]

@router.post("/")
async def create_team(team: Team, db=Depends(MongoDB.get_db())):
    """Crear un nuevo equipo."""
    db["team"].insert_one(team.dict())
    return {"message": "Equipo creado con éxito"}