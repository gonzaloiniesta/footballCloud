from fastapi import APIRouter, Depends
from app.models.match import Match
from app.database import get_db

router = APIRouter()

@router.get("/")
async def get_matches(db=Depends(get_db)):
    """Obtener la lista de partidos."""
    matches = db["matches"].find()  # Ejemplo con MongoDB
    return [match for match in matches]

@router.post("/")
async def create_match(match: Match, db=Depends(get_db)):
    """Crear un nuevo partido."""
    db["matches"].insert_one(match.dict())
    return {"message": "Partido creado con éxito"}
