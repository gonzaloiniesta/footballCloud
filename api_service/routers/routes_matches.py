from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from models import Match
from mongodb import MongoDB

router_matches = APIRouter(
    prefix="/matches",
    tags=["Matches"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

def get_db():
    db = MongoDB().get_db()
    return next(db)


# Obtener todos los partidos con filtros opcionales
@router_matches.get(
    "/",
    response_model=List[Match],
    summary="Retrieve all matches",
    description="Fetches all matches available in the database. Supports filtering with optional query parameters.",
    responses={
        200: {
            "description": "A list of matches",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "match_id": "m_001",
                            "home_team_id": "t_001",
                            "visiting_team_id": "t_002",
                            "date": "2023-11-22",
                            "score": [3, 2],
                            "possesion_home_team": 55,
                            "possesion_visiting_team": 45,
                            "cards_home_team": 2,
                            "cards_visiting_team": 3,
                            "outlines_home_team": 5,
                            "outlines_visiting_team": 4,
                            "tackles_home_team": 18,
                            "tackles_visiting_team": 14,
                            "shots_on_target_home_team": 10,
                            "shots_on_target_visitng_team": 7,
                            "balls_lost_home_team": 15,
                            "balls_lost_visiting_team": 20,
                            "completed_passes_home_team": 400,
                            "completed_passes_visiting_team": 350,
                            "players_home_team": [],
                            "players_visiting_team": []
                        }
                    ]
                }
            },
        }
    },
)
async def get_matches(
    db=Depends(get_db),
    home_team_id: Optional[str] = Query(None, description="Filter by home team ID"),
    visiting_team_id: Optional[str] = Query(None, description="Filter by visiting team ID"),
    date: Optional[str] = Query(None, description="Filter by match date (YYYY-MM-DD)"),
    limit: Optional[int] = Query(10, ge=1, description="Limit the number of results (default: 10)"),
    skip: Optional[int] = Query(0, ge=0, description="Number of results to skip (default: 0)"),
):
    """
    Retrieves all matches from the database.

    Supports filtering by `home_team_id`, `visiting_team_id`, and `date`. Allows pagination with `limit` and `skip`.
    """
    query = {}
    if home_team_id:
        query["home_team_id"] = home_team_id
    if visiting_team_id:
        query["visiting_team_id"] = visiting_team_id
    if date:
        query["date"] = date

    matches_cursor = db["matches"].find(query)

    if skip:
        matches_cursor = matches_cursor.skip(skip)
    if limit:
        matches_cursor = matches_cursor.limit(limit)

    matches = [
        {
            **match,
            "_id": str(match["_id"]),  # Convertir ObjectId a string
        }
        for match in matches_cursor
    ]

    if not matches:
        raise HTTPException(status_code=404, detail="No matches found")

    return matches


# Obtener un partido por ID
@router_matches.get(
    "/{match_id}",
    response_model=Match,
    summary="Retrieve a match by ID",
    description="Fetches the details of a specific match using its ID.",
    responses={
        200: {
            "description": "Match details",
            "content": {
                "application/json": {
                    "example": {
                        "match_id": "m_001",
                        "home_team_id": "t_001",
                        "visiting_team_id": "t_002",
                        "date": "2023-11-22",
                        "score": [3, 2],
                        "possesion_home_team": 55,
                        "possesion_visiting_team": 45,
                        "cards_home_team": 2,
                        "cards_visiting_team": 3,
                        "outlines_home_team": 5,
                        "outlines_visiting_team": 4,
                        "tackles_home_team": 18,
                        "tackles_visiting_team": 14,
                        "shots_on_target_home_team": 10,
                        "shots_on_target_visitng_team": 7,
                        "balls_lost_home_team": 15,
                        "balls_lost_visiting_team": 20,
                        "completed_passes_home_team": 400,
                        "completed_passes_visiting_team": 350,
                        "players_home_team": [],
                        "players_visiting_team": []
                    }
                }
            },
        },
        404: {"description": "Match not found"},
    },
)
async def get_match_by_id(
    match_id: str = Path(..., description="The ID of the match"),
    db=Depends(get_db),
):
    """
    Retrieves a specific match by its ID.

    **Path Parameter**:
    - `match_id`: The ID of the match to retrieve.
    """
    match = db["matches"].find_one({"match_id": match_id})
    
    if not match:
        raise HTTPException(status_code=404, detail=f"Match with ID '{match_id}' not found")

    match["_id"] = str(match["_id"])  # Convertir ObjectId a string

    return match
