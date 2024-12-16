from fastapi import FastAPI
from routers import router_matches

app = FastAPI(
    title="Football Analytics API",
    description="API para análisis estadístico de partidos de fútbol",
    version="1.0.0"
)

# Matches routes
app.include_router(router_matches)

# Players routes
# app.include_router(router_players)

# Teams routes
# app.include_router(router_teams)

# Leagues routes
# app.include_router(router_league)
