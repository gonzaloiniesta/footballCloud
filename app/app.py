from fastapi import FastAPI
from routers import router_league, router_team, router_match, router_player

app = FastAPI(
    title="Football Analytics API",
    description="API para análisis estadístico de partidos de fútbol",
    version="1.0.0"
)


# Matches routes
app.include_router(router_match, prefix="/matches", tags=["Matches"])

# Players routes
app.include_router(router_player, prefix="/players", tags=["Players"])

# Teams routes
app.include_router(router_team, prefix="/teams", tags=["Teams"])

# Leagues routes
app.include_router(router_league, prefix="/leagues", tags=["Leagues"])



@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Football Analytics API!"}
