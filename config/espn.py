""" Handles configuration for data from ESPN. """
# maps the column names and types for defense passing
defense_passing_map = {
    "team": str,
    "games": int,
    "passing_cmp_against": int,
    "passing_att_against": int,
    "passing_cmp_percent_against": float,
    "passing_yds_against": int,
    "passing_ya_against": float,
    "passing_yds_per_game_against": float,
    "passing_longest_pass_against": int,
    "passing_td_against": int,
    "passing_int_against": int,
    "passing_sack_against": int,
    "sack_yards_lost": int,
    "passer_rating": float
}

# maps the column names and types for defense rushing
defense_rushing_map = {
    "team": str,
    "games": int,
    "rushing_att_against": int,
    "rushing_yds_against": int,
    "rushing_ya_against": float,
    "rushing_yds_per_game_against": float,
    "rushing_longest_rush_against": int,
    "rushing_td_against": int,
    "rushing_fumbles": int,
    "rushing_fumbles_lost": int
}

# maps the column names and types for defense receiving
defense_receiving_map = {
    "team": str,
    "games": int,
    "receiving_rec_against": int,
    "receiving_yds_against": int,
    "receiving_yr_against": float,
    "receiving_yds_per_game_against": float,
    "receiving_longest_rec_against": int,
    "receiving_td_against": int,
    "receiving_fumbles": int,
    "receiving_fumbles_lost": int
}

# maps the column names and types for defense downs
defense_downs_map = {
    "team": str,
    "games": int,
    "first_downs_total_against": int,
    "first_downs_rush_against": int,
    "first_downs_pass_against": int,
    "first_downs_penalty_against": int,
    "third_downs_made_against": int,
    "third_downs_att_against": int,
    "third_downs_percentage_against": float,
    "fourth_downs_made_against": int,
    "fourth_downs_att_against": int,
    "fourth_downs_percentage_against": float,
    "penalties": int,
    "penalties_yds": int
}

# maps the column names and types for offense passing
offense_passing_map = {
    "team": str,
    "games": int,
    "passing_cmp": int,
    "passing_att": int,
    "passing_cmp_percent": float,
    "passing_yds": int,
    "passing_ya": float,
    "passing_yds_per_game": float,
    "passing_longest_pass": int,
    "passing_td": int,
    "passing_int": int,
    "passing_sack": int,
    "sack_yards_lost": int,
    "passer_rating": float
}

# maps the column names and types for offense rushing
offense_rushing_map = {
    "team": str,
    "games": int,
    "rushing_att": int,
    "rushing_yds": int,
    "rushing_ya": float,
    "rushing_yds_per_game": float,
    "rushing_longest_rush": int,
    "rushing_td": int,
    "rushing_fumbles": int,
    "rushing_fumbles_lost": int
}

# maps the column names and types for offense receiving
offense_receiving_map = {
    "team": str,
    "games": int,
    "receiving_rec": int,
    "receiving_yds": int,
    "receiving_yr": float,
    "receiving_yds_per_game": float,
    "receiving_longest_rec": int,
    "receiving_td": int,
    "receiving_fumbles": int,
    "receiving_fumbles_lost": int
}

# maps the column names and types for defense downs
offense_downs_map = {
    "team": str,
    "games": int,
    "first_downs_total": int,
    "first_downs_rush": int,
    "first_downs_pass": int,
    "first_downs_penalty": int,
    "third_downs_made": int,
    "third_downs_att": int,
    "third_downs_percentage": float,
    "fourth_downs_made": int,
    "fourth_downs_att": int,
    "fourth_downs_percentage": float,
    "penalties": int,
    "penalties_yds": int
}
