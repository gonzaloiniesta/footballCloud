from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from models import League
from mongodb import MongoDB

router_league = APIRouter(
    prefix="/leagues",
    tags=["Leagues"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

def get_db():
    db = MongoDB().get_db()
    return next(db)

@router_league.get(
    "",
    response_model=List[League],
    summary="Retrieve all leagues",
    description="Fetches all the leagues available in the database. Supports filtering with optional query parameters.",
    responses={
        200: {
            "description": "A list of leagues",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "league_id" : "0001",
                            "name" : "LaLiga",
                            "country" : "Spain",
                            "classification_league" : [
                                "0101", 
                                "0102",
                                "0103",
                                "0104",
                                "0105",
                                "0106",
                                "0107",
                                "0108",
                                "0109",
                                "0110"
                            ]
                        }
                    ]
                }
            },
        }
    },
)
async def get_league(
    db=Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by league name"),
    country: Optional[str] = Query(None, description="Filter by country"),
    limit: Optional[int] = Query(10, ge=1, description="Limit the number of results (default: 10)"),
    skip: Optional[int] = Query(0, ge=0, description="Number of results to skip (default: 0)"),
):
    """
    Retrieves all leagues from the database.

    Supports filtering by `name` and `country`, and allows pagination with `limit` and `skip`.
    """
    query = {}
    if name:
        query["name"] = name
    if country:
        query["country"] = country

    leagues_cursor = db["leagues"].find(query)

    if skip:
        leagues_cursor = leagues_cursor.skip(skip)
    if limit:
        leagues_cursor = leagues_cursor.limit(limit)

    response = [
        {
            **league,
            "_id": str(league["_id"]),
        }
        for league in leagues_cursor
    ]

    if not response:
        raise HTTPException(status_code=404, detail="No leagues found")

    return response



@router_league.get(
    "/{league_id}",
    summary="Get information in a league",
    description="Fetches the information of a specific league using the league ID.",
    responses={
        200: {
            "description": "List of team IDs in the league",
            "content": {
                "application/json": {
                    "example": {
                        "league_id": "0001",
                        "name": "LaLiga",
                        "teams": ["0101", "0102", "0103", "0104"]
                    }
                }
            },
        },
        404: {"description": "League not found"},
    },
)
async def get_league_info_by_id(
    league_id: str = Path(..., description="The ID of the league"),
    db=Depends(get_db),
):
    """
    Retrieves the list of teams associated with a specific league using the `league_id`.

    **Path Parameter**:
    - `league_id`: The ID of the league whose teams you want to retrieve.

    **Returns**:
    - A JSON object containing the league ID, name, and the list of team IDs.
    """

    league = db["leagues"].find_one({"league_id": league_id})
    
    if not league:
        raise HTTPException(status_code=404, detail=f"League with ID '{league_id}' not found")
    

    response = {
        "league_id": league["league_id"],
        "name": league["name"],
        "teams": league["classification_league"],
    }
    
    return response


@router_league.get(
    "/{league_id}/classification",
    response_model=List[dict],
    summary="Get league classification",
    description="Fetches the classification of teams in a specific league using the league ID.",
    responses={
        200: {
            "description": "List of teams in the league classification",
            "content": {
                "application/json": {
                    "example": [
                        {"classification": 1, "team_name": "Real Madrid"},
                        {"classification": 2, "team_name": "Barcelona"},
                        {"classification": 3, "team_name": "Atletico Madrid"}
                    ]
                }
            },
        },
        404: {"description": "League or teams not found"},
    },
)
async def get_league_classification(
    league_id: str = Path(..., description="The ID of the league"),
    db=Depends(get_db),
):
    """
    Retrieves the classification of teams in a specific league by its `league_id`.

    **Path Parameter**:
    - `league_id`: The ID of the league.

    **Returns**:
    - A JSON array containing the classification and team names.
    """
    
    league = db["leagues"].find_one({"league_id": league_id})
    if not league:
        raise HTTPException(status_code=404, detail=f"League with ID '{league_id}' not found")

    
    teams_cursor = db["teams"].find({"league": league["name"]}).sort("classification", 1)
    classification = [
        {"classification": team["classification"], "team_name": team["name"]}
        for team in teams_cursor
    ]

    if not classification:
        raise HTTPException(status_code=404, detail=f"No teams found for league with ID '{league_id}'")

    return classification




@router_league.get(
    "/{league_id}/teams",
    response_model=List[dict],
    summary="Get teams in a league",
    description="Fetches the identifiers and names of teams in a specific league using the league ID.",
    responses={
        200: {
            "description": "List of team identifiers and names",
            "content": {
                "application/json": {
                    "example": [
                        {"team_id": "001", "team_name": "Real Madrid"},
                        {"team_id": "002", "team_name": "Barcelona"},
                        {"team_id": "003", "team_name": "Atletico Madrid"}
                    ]
                }
            },
        },
        404: {"description": "League or teams not found"},
    },
)
async def get_teams_in_league(
    league_id: str = Path(..., description="The ID of the league"),
    db=Depends(get_db),
):
    """
    Retrieves the list of team identifiers and names associated with a specific league using the `league_id`.

    **Path Parameter**:
    - `league_id`: The ID of the league.

    **Returns**:
    - A JSON array containing the `team_id` and `team_name` of each team in the league.
    """
    # Verificar que la liga existe
    league = db["leagues"].find_one({"league_id": league_id})
    if not league:
        raise HTTPException(status_code=404, detail=f"League with ID '{league_id}' not found")

    # Obtener equipos de la liga
    teams_cursor = db["teams"].find({"league": league["name"]})
    teams = [
        {"team_id": team["team_id"], "team_name": team["name"]}
        for team in teams_cursor
    ]

    if not teams:
        raise HTTPException(status_code=404, detail=f"No teams found for league with ID '{league_id}'")

    return teams

