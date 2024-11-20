import random
import json
from datetime import datetime, timedelta
import numpy as np
from itertools import combinations

# Generador de IDs
def generate_id(prefix, num):
    return f"{prefix}_{str(num).zfill(4)}"

# Generar valores con distribución normal
def random_normal(mean, std_dev, min_val, max_val):
    value = int(np.random.normal(mean, std_dev))
    return max(min(value, max_val), min_val)

# Generador de jugadores
def generate_player(player_id, team_id):
    return {
        "player_id": player_id,
        "name": f"Player{player_id[-4:]}",
        "surname": f"Surname{player_id[-4:]}",
        "nacionality": random.choice(["Spain", "France", "Germany", "Italy", "England"]),
        "team_id": team_id,
        "total_goals": 0,
        "total_cards": 0,
        "total_minutes": 0,
        "total_outlines": 0,
        "total_tackles": 0,
        "total_shots_on_target": 0,
        "total_dribbles": 0,
        "total_balls_lost": 0,
        "total_completed_passes": 0
    }

# Generador de equipos
def generate_team(team_id, league_name, country, player_ids):
    return {
        "team_id": team_id,
        "name": f"Team{team_id[-4:]}",
        "league": league_name,
        "country": country,
        "goals_for": 0,
        "goals_against": 0,
        "cards": 0,
        "players": player_ids
    }

# Generador de ligas
def generate_league(league_id, country, team_ids):
    return {
        "league_id": league_id,
        "name": f"League{league_id}",
        "country": country,
        "classification_league": team_ids
    }

# Actualizar estadísticas de jugadores
def update_player_stats(player, stats):
    player["total_goals"] += stats["goals"]
    player["total_cards"] += stats["cards"]
    player["total_minutes"] += stats["minutes"]
    player["total_outlines"] += stats["outlines"]
    player["total_tackles"] += stats["tackles"]
    player["total_shots_on_target"] += stats["shots_on_target"]
    player["total_dribbles"] += stats["dribbles"]
    player["total_balls_lost"] += stats["balls_lost"]
    player["total_completed_passes"] += stats["completed_passes"]

# Generador de partidos
def generate_match(match_id, home_team, visiting_team, home_players, visiting_players, date, all_players):
    def generate_player_stats(player_id):
        return {
            "player_id": player_id,
            "goals": random_normal(0.2, 0.5, 0, 2),
            "cards": random_normal(0.1, 0.3, 0, 1),
            "minutes": random.randint(60, 90),
            "outlines": random.randint(0, 5),
            "tackles": random.randint(0, 10),
            "shots_on_target": random_normal(1, 2, 0, 5),
            "dribbles": random.randint(0, 8),
            "balls_lost": random.randint(0, 5),
            "completed_passes": random.randint(20, 50)
        }

    # Estadísticas de jugadores
    home_players_stats = [generate_player_stats(player["player_id"]) for player in home_players]
    visiting_players_stats = [generate_player_stats(player["player_id"]) for player in visiting_players]

    # Calcular totales
    home_score = sum(player["goals"] for player in home_players_stats)
    visiting_score = sum(player["goals"] for player in visiting_players_stats)

    # Actualizar estadísticas de los equipos
    home_team["goals_for"] += home_score
    home_team["goals_against"] += visiting_score
    visiting_team["goals_for"] += visiting_score
    visiting_team["goals_against"] += home_score

    home_team["cards"] += sum(player["cards"] for player in home_players_stats)
    visiting_team["cards"] += sum(player["cards"] for player in visiting_players_stats)

    # Actualizar estadísticas de los jugadores
    for stats in home_players_stats:
        player = next(p for p in all_players if p["player_id"] == stats["player_id"])
        update_player_stats(player, stats)

    for stats in visiting_players_stats:
        player = next(p for p in all_players if p["player_id"] == stats["player_id"])
        update_player_stats(player, stats)

    return {
        "match_id": match_id,
        "home_team_id": home_team["team_id"],
        "visiting_team_id": visiting_team["team_id"],
        "date": date,
        "score": [home_score, visiting_score],
        "cards_home_team": sum(player["cards"] for player in home_players_stats),
        "cards_visiting_team": sum(player["cards"] for player in visiting_players_stats),
        "outlines_home_team": sum(player["outlines"] for player in home_players_stats),
        "outlines_visiting_team": sum(player["outlines"] for player in visiting_players_stats),
        "tackles_home_team": sum(player["tackles"] for player in home_players_stats),
        "tackles_visiting_team": sum(player["tackles"] for player in visiting_players_stats),
        "shots_on_target_home_team": sum(player["shots_on_target"] for player in home_players_stats),
        "shots_on_target_visitng_team": sum(player["shots_on_target"] for player in visiting_players_stats),
        "balls_lost_home_team": sum(player["balls_lost"] for player in home_players_stats),
        "balls_lost_visiting_team": sum(player["balls_lost"] for player in visiting_players_stats),
        "completed_passes_home_team": sum(player["completed_passes"] for player in home_players_stats),
        "completed_passes_visiting_team": sum(player["completed_passes"] for player in visiting_players_stats),
        "players_home_team": home_players_stats,
        "players_visiting_team": visiting_players_stats
    }

# Generar datos
def generate_data():
    # Configuración
    num_teams = 10
    num_players_per_team = 15
    league_id = "0001"
    league_country = "Spain"

    # Equipos y jugadores
    teams = []
    players = []
    for team_num in range(1, num_teams + 1):
        team_id = generate_id("t", team_num)
        player_ids = [generate_id("p", (team_num - 1) * num_players_per_team + i + 1) for i in range(num_players_per_team)]
        for player_id in player_ids:
            players.append(generate_player(player_id, team_id))
        teams.append(generate_team(team_id, f"League{league_id}", league_country, player_ids))

    # Liga
    league = generate_league(league_id, league_country, [team["team_id"] for team in teams])

    # Generar combinaciones de partidos (todos contra todos)
    matches = []
    start_date = datetime(2024, 1, 1)
    match_num = 1
    for home_team, visiting_team in combinations(teams, 2):
        for _ in range(2):  # Cada equipo juega como local y visitante
            match_id = generate_id("match", match_num)
            home_players = random.sample([p for p in players if p["team_id"] == home_team["team_id"]], 11)
            visiting_players = random.sample([p for p in players if p["team_id"] == visiting_team["team_id"]], 11)
            match_date = (start_date + timedelta(days=match_num * 7)).strftime("%Y-%m-%d")
            matches.append(generate_match(match_id, home_team, visiting_team, home_players, visiting_players, match_date, players))
            match_num += 1

    # Resultados
    return {
        "players": players,
        "teams": teams,
        "league": league,
        "matches": matches
    }

# Generar y guardar datos
data = generate_data()
with open("football_data.json", "w") as f:
    json.dump(data, f, indent=4)
print("Datos generados y guardados en football_data.json")
