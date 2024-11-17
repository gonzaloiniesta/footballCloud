from fastapi import APIRouter, Depends
from app.models.player import Player
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_players(db=Depends(get_db)):
    """Obtener la lista de partidos."""
    players = db["players"].find()  # Ejemplo con MongoDB
    return [player for player in players]

@router.post("/")
async def create_player(player: Player, db=Depends(get_db)):
    """Crear un nuevo partido."""
    db["players"].insert_one(player.dict())
    return {"message": "Juagdor creado con éxito"}