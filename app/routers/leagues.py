from fastapi import APIRouter, Depends
from models import League
from mongodb import MongoDB

router = APIRouter()

@router.get("/")
async def get_leagues(db=Depends(MongoDB().get_db())):
    """Obtener la lista de partidos."""
    matches = db["league"].find()  # Ejemplo con MongoDB
    return [match for match in matches]

@router.post("/")
async def create_league(match: League, db=Depends(MongoDB().get_db())):
    """Crear una nueva Liga."""
    db["league"].insert_one(match.dict())
    return {"message": "Liga creada con éxito"}
