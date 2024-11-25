from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from models import Team, Player
from mongodb import MongoDB

router_teams= APIRouter(
    prefix="/teams",
    tags=["Teams"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

def get_db():
    db = MongoDB().get_db()
    return next(db)

# Obtener todos los equipos con filtros opcionales
@router_teams.get(
    "/",
    response_model=List[Team],
    summary="Retrieve all teams",
    description="Fetches all the teams available in the database. Supports filtering with optional query parameters.",
    responses={
        200: {
            "description": "A list of teams",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "team_id": "001",
                            "name": "Real Madrid",
                            "league": "LaLiga",
                            "country": "Spain",
                            "classification": 1,
                            "points": 78,
                            "wins": 25,
                            "draws": 3,
                            "loses": 5,
                            "goals_for": 75,
                            "goals_against": 30,
                            "players": ["101", "102", "103"]
                        }
                    ]
                }
            },
        }
    },
)
async def get_teams(
    db=Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by team name"),
    league: Optional[str] = Query(None, description="Filter by league"),
    country: Optional[str] = Query(None, description="Filter by country"),
    limit: Optional[int] = Query(10, ge=1, description="Limit the number of results (default: 10)"),
    skip: Optional[int] = Query(0, ge=0, description="Number of results to skip (default: 0)"),
):
    """
    Retrieves all teams from the database.

    Supports filtering by `name`, `league`, and `country`. Allows pagination with `limit` and `skip`.
    """
    query = {}
    if name:
        query["name"] = name
    if league:
        query["league"] = league
    if country:
        query["country"] = country

    teams_cursor = db["teams"].find(query)

    if skip:
        teams_cursor = teams_cursor.skip(skip)
    if limit:
        teams_cursor = teams_cursor.limit(limit)

    response = [
        {
            **team,
            "_id": str(team["_id"]),
        }
        for team in teams_cursor
    ]

    if not response:
        raise HTTPException(status_code=404, detail="No teams found")

    return response


@router_teams.get(
    "/{team_id}",
    response_model=Team,
    summary="Retrieve a team by ID",
    description="Fetches the details of a specific team using the team ID.",
    responses={
        200: {
            "description": "The team details",
            "content": {
                "application/json": {
                    "example": {
                        "team_id": "001",
                        "name": "Real Madrid",
                        "league": "LaLiga",
                        "country": "Spain",
                        "classification": 1,
                        "points": 78,
                        "wins": 25,
                        "draws": 3,
                        "loses": 5,
                        "goals_for": 75,
                        "goals_against": 30,
                        "players": ["101", "102", "103"]
                    }
                }
            },
        },
        404: {"description": "Team not found"},
    },
)
async def get_team_by_id(
    team_id: str = Path(..., description="The ID of the team"),
    db=Depends(get_db),
):
    """
    Retrieves a specific team by its `team_id`.

    **Path Parameter**:
    - `team_id`: The ID of the team to retrieve.
    """
    team = db["teams"].find_one({"team_id": team_id})
    
    if not team:
        raise HTTPException(status_code=404, detail=f"Team with ID '{team_id}' not found")
    
    team["_id"] = str(team["_id"])  # Convertir ObjectId a string

    return team


@router_teams.get(
    "/{team_id}/players",
    response_model=List[Player],
    summary="Get players of a team",
    description="Fetches the list of players in a specific team using the team ID.",
    responses={
        200: {
            "description": "List of players in the team",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "player_id": "101",
                            "name": "Karim",
                            "surname": "Benzema",
                            "nacionality": "France",
                            "team_id": "001",
                            "total_goals": 20,
                            "total_cards": 3,
                            "total_minutes": 1800,
                            "total_outlines": 5,
                            "total_tackles": 10,
                            "total_shots_on_target": 25,
                            "total_dribbles": 15,
                            "total_balls_lost": 10,
                            "total_completed_passes": 300
                        }
                    ]
                }
            },
        },
        404: {"description": "Team or players not found"},
    },
)
async def get_players_by_team(
    team_id: str = Path(..., description="The ID of the team"),
    db=Depends(get_db),
):
    """
    Retrieves the list of players associated with a specific team using the `team_id`.

    **Path Parameter**:
    - `team_id`: The ID of the team whose players you want to retrieve.

    **Returns**:
    - A JSON array of player objects.
    """
    players_cursor = db["players"].find({"team_id": team_id})
    players = [
        {
            **player,
            "_id": str(player["_id"]),
        }
        for player in players_cursor
    ]

    if not players:
        raise HTTPException(status_code=404, detail=f"No players found for team with ID '{team_id}'")

    return players
