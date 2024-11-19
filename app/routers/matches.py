from fastapi import APIRouter, Depends
from models import Match
from mongodb import MongoDB

router = APIRouter()

@router.get("/")
async def get_matches(db=Depends(MongoDB.get_db())):
    """Obtener la lista de partidos."""
    matches = db["matches"].find()  # Ejemplo con MongoDB
    return [match for match in matches]

@router.post("/")
async def create_match(match: Match, db=Depends(MongoDB.get_db())):
    """Crear un nuevo partido."""
    db["matches"].insert_one(match.dict())
    return {"message": "Partido creado con éxito"}
