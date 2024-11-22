from fastapi import FastAPI
try:
    from app.routers import get_leagues, get_matches, get_players, get_teams, create_league, create_match, create_player, create_team
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    raise


app = FastAPI(
    title="Football Analytics API",
    description="API para análisis estadístico de partidos de fútbol",
    version="1.0.0"
)

# Matches routes
app.include_router(get_matches, prefix="/matches", tags=["Matches"])
app.include_router(create_match, prefix="/matches", tags=["Matches_POST"])

# Players routes
app.include_router(get_players, prefix="/players", tags=["Players"])
app.include_router(create_league, prefix="/players", tags=["Players_POST"])

# Teams routes
app.include_router(get_teams, prefix="/teams", tags=["Teams"])
app.include_router(get_teams, prefix="/teams", tags=["Teams_POST"])

# Leagues routes
app.include_router(get_leagues, prefix="/league", tags=["Leagues"])
app.include_router(create_league, prefix="/league", tags=["Leagues_POST"])


@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Football Analytics API!"}
