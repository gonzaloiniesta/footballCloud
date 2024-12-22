
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE attack_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
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
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
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

CREATE TABLE match_results_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
    matches_won INT,
    matches_lost INT,
    matches_drawn INT,
    goals_scored INT,
    goals_conceded INT,
    own_goals INT
);

CREATE TABLE defensive_statistics (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
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
    team_id INT REFERENCES teams(team_id) ON DELETE CASCADE,
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
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
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
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
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
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
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
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
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
    player_id INT REFERENCES players(player_id) ON DELETE CASCADE,
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
