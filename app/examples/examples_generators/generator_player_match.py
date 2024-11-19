import random, json
from models import Match, PlayerMatch


# Generate a match with 13 players per team and consistent stats
def generate_match_with_players(match_id, home_team_id, visiting_team_id, match_date):
    total_goals_home = random.randint(1, 5)
    total_goals_away = random.randint(0, 4)
    total_cards_home = random.randint(1, 5)
    total_cards_away = random.randint(1, 5)
    
    players_home = [f"p_{i:04d}" for i in range(1, 14)]  # 13 players
    players_away = [f"p_{i:04d}" for i in range(14, 27)]  # 13 players
    
    # Distribute goals among players
    goals_home_distribution = [0] * len(players_home)
    goals_away_distribution = [0] * len(players_away)
    
    for _ in range(total_goals_home):
        goals_home_distribution[random.randint(0, len(players_home) - 1)] += 1

    for _ in range(total_goals_away):
        goals_away_distribution[random.randint(0, len(players_away) - 1)] += 1

    # Generate players for home team
    players_home_team = [
        PlayerMatch(
            player_id=player_id,
            goals=goals_home_distribution[i],
            cards=random.randint(0, 1),
            minutes=random.randint(60, 90),
            outlines=random.randint(0, 3),
            tackles=random.randint(2, 6),
            shots_on_target=random.randint(1, 5),
            dribbles=random.randint(1, 5),
            balls_lost=random.randint(0, 5),
            completed_passes=random.randint(20, 50)
        )
        for i, player_id in enumerate(players_home)
    ]

    # Generate players for visiting team
    players_visiting_team = [
        PlayerMatch(
            player_id=player_id,
            goals=goals_away_distribution[i],
            cards=random.randint(0, 1),
            minutes=random.randint(60, 90),
            outlines=random.randint(0, 3),
            tackles=random.randint(2, 6),
            shots_on_target=random.randint(1, 5),
            dribbles=random.randint(1, 5),
            balls_lost=random.randint(0, 5),
            completed_passes=random.randint(20, 50)
        )
        for i, player_id in enumerate(players_away)
    ]

    return Match(
        match_id=match_id,
        home_team_id=home_team_id,
        visiting_team_id=visiting_team_id,
        date=match_date,
        score=(total_goals_home, total_goals_away),
        cards_home_team=total_cards_home,
        cards_visiting_team=total_cards_away,
        outlines_home_team=sum(player.outlines for player in players_home_team),
        outlines_visiting_team=sum(player.outlines for player in players_visiting_team),
        tackles_home_team=sum(player.tackles for player in players_home_team),
        tackles_visiting_team=sum(player.tackles for player in players_visiting_team),
        shots_on_target_home_team=sum(player.shots_on_target for player in players_home_team),
        shots_on_target_visitng_team=sum(player.shots_on_target for player in players_visiting_team),
        balls_lost_home_team=sum(player.balls_lost for player in players_home_team),
        balls_lost_visiting_team=sum(player.balls_lost for player in players_visiting_team),
        completed_passes_home_team=sum(player.completed_passes for player in players_home_team),
        completed_passes_visiting_team=sum(player.completed_passes for player in players_visiting_team),
        players_home_team=players_home_team,
        players_visiting_team=players_visiting_team
    )

# Generate a sample match
match_sample = generate_match_with_players(
    match_id="match_001",
    home_team_id="t_0001",
    visiting_team_id="t_0002",
    match_date="2024-11-18"
)

with open('/Users/giniest/FootballAnalytics/footballAnalytics/app/examples/match.example.json', 'w') as file:
    json.dump(match_sample.dict(), file, indent=4)

