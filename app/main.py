from fastapi import FastAPI
from app.routers import matches, players

app = FastAPI(
    title="Football Analytics API",
    description="API para análisis estadístico de partidos de fútbol",
    version="1.0.0"
)

# Incluir rutas
app.include_router(matches.router, prefix="/matches", tags=["Matches"])
app.include_router(players.router, prefix="/players", tags=["Players"])

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Football Analytics API!"}
