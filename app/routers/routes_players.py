from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from models import Player
from mongodb import MongoDB

router_players = APIRouter(
    prefix="/players",
    tags=["Players"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

def get_db():
    db = MongoDB().get_db()
    return next(db)

# Obtener todos los jugadores con filtros opcionales
@router_players.get(
    "",
    response_model=List[Player],
    summary="Retrieve all players",
    description="Fetches all players available in the database. Supports filtering with optional query parameters.",
    responses={
        200: {
            "description": "A list of players",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "player_id": "p_001",
                            "name": "Lionel",
                            "surname": "Messi",
                            "nacionality": "Argentina",
                            "team_id": "t_001",
                            "total_goals": 30,
                            "total_cards": 2,
                            "total_minutes": 2700,
                            "total_outlines": 10,
                            "total_tackles": 20,
                            "total_shots_on_target": 50,
                            "total_dribbles": 70,
                            "total_balls_lost": 15,
                            "total_completed_passes": 500
                        }
                    ]
                }
            },
        }
    },
)
async def get_players(
    db=Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by player name"),
    team_id: Optional[str] = Query(None, description="Filter by team ID"),
    nacionality: Optional[str] = Query(None, description="Filter by nationality"),
    limit: Optional[int] = Query(10, ge=1, description="Limit the number of results (default: 10)"),
    skip: Optional[int] = Query(0, ge=0, description="Number of results to skip (default: 0)"),
):
    """
    Retrieves all players from the database.

    Supports filtering by `name`, `team_id`, and `nacionality`. Allows pagination with `limit` and `skip`.
    """
    query = {}
    if name:
        query["name"] = name
    if team_id:
        query["team_id"] = team_id
    if nacionality:
        query["nacionality"] = nacionality

    players_cursor = db["players"].find(query)

    if skip:
        players_cursor = players_cursor.skip(skip)
    if limit:
        players_cursor = players_cursor.limit(limit)

    players = [
        {
            **player,
            "_id": str(player["_id"]),  # Convertir ObjectId a string
        }
        for player in players_cursor
    ]

    if not players:
        raise HTTPException(status_code=404, detail="No players found")

    return players



@router_players.get(
    "/{player_id}",
    response_model=Player,
    summary="Retrieve a player by ID",
    description="Fetches the details of a specific player using their ID.",
    responses={
        200: {
            "description": "Player details",
            "content": {
                "application/json": {
                    "example": {
                        "player_id": "p_001",
                        "name": "Lionel",
                        "surname": "Messi",
                        "nacionality": "Argentina",
                        "team_id": "t_001",
                        "total_goals": 30,
                        "total_cards": 2,
                        "total_minutes": 2700,
                        "total_outlines": 10,
                        "total_tackles": 20,
                        "total_shots_on_target": 50,
                        "total_dribbles": 70,
                        "total_balls_lost": 15,
                        "total_completed_passes": 500
                    }
                }
            },
        },
        404: {"description": "Player not found"},
    },
)
async def get_player_by_id(
    player_id: str = Path(..., description="The ID of the player"),
    db=Depends(get_db),
):
    """
    Retrieves a player by their ID.

    **Path Parameter**:
    - `player_id`: The ID of the player to retrieve.
    """
    player = db["players"].find_one({"player_id": player_id})
    
    if not player:
        raise HTTPException(status_code=404, detail=f"Player with ID '{player_id}' not found")

    player["_id"] = str(player["_id"])  # Convertir ObjectId a string

    return player