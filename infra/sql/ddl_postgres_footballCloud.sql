-- Drop existing tables to ensure a clean setup
DROP TABLE IF EXISTS player_attack_statistics CASCADE;
DROP TABLE IF EXISTS player_efficiency_statistics CASCADE;
DROP TABLE IF EXISTS player_defensive_statistics CASCADE;
DROP TABLE IF EXISTS player_classic_statistics CASCADE;
DROP TABLE IF EXISTS player_discipline_statistics CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS efficiency_statistics CASCADE;
DROP TABLE IF EXISTS defensive_statistics CASCADE;
DROP TABLE IF EXISTS classic_statistics CASCADE;
DROP TABLE IF EXISTS discipline_statistics CASCADE;
DROP TABLE IF EXISTS attack_statistics CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS leagues CASCADE;

-- Create tables
CREATE TABLE leagues (
    league_id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    league_id INT REFERENCES leagues(league_id)
);

CREATE TABLE attack_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    shots INT,
    shots_on_target INT,
    assists INT,
    successful_dribbles INT,
    failed_dribbles INT,
    goals INT,
    goals_inside_box INT,
    goals_outside_box INT,
    left_foot_goals FLOAT,
    right_foot_goals FLOAT,
    penalty_goals INT,
    header_goals FLOAT,
    set_piece_goals FLOAT,
    own_goals INT
);

CREATE TABLE discipline_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    yellow_cards INT,
    red_cards INT,
    second_yellows INT,
    offsides INT,
    fouls_suffered INT,
    fouls_committed INT,
    penalties_won INT,
    penalties_committed INT,
    handballs INT,
    fouls_per_card FLOAT
);

CREATE TABLE classic_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    matches_won INT,
    matches_lost INT,
    matches_drawn INT,
    goals_scored INT,
    goals_conceded INT,
    own_goals INT
);

CREATE TABLE defensive_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    blocks INT,
    interceptions INT,
    recoveries INT,
    clearances INT,
    successful_tackles INT,
    failed_tackles INT,
    last_man_tackles INT,
    successful_duels INT,
    failed_duels INT,
    successful_aerial_duels INT,
    failed_aerial_duels INT
);

CREATE TABLE efficiency_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    corners_taken INT,
    tackles INT,
    duels INT,
    body_duels INT,
    aerial_duels INT,
    passes INT,
    short_passes INT,
    long_passes INT,
    through_passes INT,
    goals_per_shot FLOAT,
    goals_per_shot_outside_box FLOAT,
    goals_per_shot_inside_box FLOAT,
    left_foot_goals FLOAT,
    right_foot_goals FLOAT,
    header_goals FLOAT,
    set_piece_goals FLOAT
);

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    team_id INT REFERENCES teams(team_id)
);

CREATE TABLE player_discipline_statistics (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    yellow_cards INT,
    red_cards INT,
    second_yellows INT,
    offsides INT,
    fouls_suffered INT,
    fouls_committed INT,
    penalties_won INT,
    penalties_committed INT,
    handballs INT,
    fouls_per_card FLOAT
);

CREATE TABLE player_classic_statistics (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    minutes_played INT,
    matches_played INT,
    complete_matches INT,
    starting_matches INT,
    substituted_matches INT,
    goals INT,
    penalties_won INT,
    own_goals INT,
    goals_conceded INT
);

CREATE TABLE player_defensive_statistics (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    blocks INT,
    interceptions INT,
    recoveries INT,
    clearances INT,
    successful_tackles INT,
    failed_tackles INT,
    last_man_tackles INT,
    successful_duels INT,
    failed_duels INT,
    successful_aerial_duels INT,
    failed_aerial_duels INT
);

CREATE TABLE player_efficiency_statistics (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    corners_taken INT,
    tackles INT,
    duels INT,
    body_duels INT,
    aerial_duels INT,
    passes INT,
    short_passes INT,
    long_passes INT,
    through_passes INT,
    goals_per_shot FLOAT,
    goals_per_shot_outside_box FLOAT,
    goals_per_shot_inside_box FLOAT,
    left_foot_goals FLOAT,
    right_foot_goals FLOAT,
    header_goals FLOAT,
    set_piece_goals FLOAT
);

CREATE TABLE player_attack_statistics (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    shots INT,
    shots_on_target INT,
    assists INT,
    successful_dribbles INT,
    failed_dribbles INT,
    goals INT,
    goals_inside_box INT,
    goals_outside_box INT,
    left_foot_goals FLOAT,
    right_foot_goals FLOAT,
    penalty_goals INT,
    header_goals FLOAT,
    set_piece_goals FLOAT,
    own_goals INT
);
