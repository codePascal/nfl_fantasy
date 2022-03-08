""" Handles configuration for data from ESPN.

Glossary for help:
https://www.hometeamsonline.com/teams/popups/Glossary.asp?s=football
"""
# maps the column names and types for defense passing
defense_passing_map = {
    "team": str,
    "games_defense": float,
    "passing_cmp_allowed": float,
    "passing_att_allowed": float,
    "passing_cmppct_allowed": float,
    "passing_yds_allowed": float,
    "passing_avg_allowed": float,
    "passing_yds_allowed_per_game": float,
    "passing_longest_allowed": float,
    "passing_td_allowed": float,
    "ints": float,
    "sacks": float,
    "sack_yards_gained": float,
    "passer_rating": float
}

# maps the column names and types for defense rushing
defense_rushing_map = {
    "team": str,
    "games_defense": float,
    "rushing_att_allowed": float,
    "rushing_yds_allowed": float,
    "rushing_avg_allowed": float,
    "rushing_yds_allowed_per_game": float,
    "rushing_longest_allowed": float,
    "rushing_td_allowed": float,
    "rushing_fumbles": float,
    "rushing_fumbles_lost": float
}

# maps the column names and types for defense receiving
defense_receiving_map = {
    "team": str,
    "games_defense": float,
    "receiving_rec_allowed": float,
    "receiving_yds_allowed": float,
    "receiving_avg_allowed": float,
    "receiving_yds_allowed_per_game": float,
    "receiving_longest_allowed": float,
    "receiving_td_allowed": float,
    "receiving_fumbles": float,
    "receiving_fumbles_lost": float
}

# maps the column names and types for defense downs
defense_downs_map = {
    "team": str,
    "games_defense": float,
    "1st_total_allowed": float,
    "1st_rush_allowed": float,
    "1st_pass_allowed": float,
    "1st_penalty_allowed": float,
    "3rd_conv_allowed": float,
    "3rd_att_allowed": float,
    "3rd_pct_allowed": float,
    "4th_conv_allowed": float,
    "4th_att_allowed": float,
    "4th_pct_allowed": float,
    "defense_penalties": float,
    "defense_yds_lost": float
}

# maps the column names and types for offense passing
offense_passing_map = {
    "team": str,
    "games_offense": float,
    "passing_cmp_offense": float,
    "passing_att_offense": float,
    "passing_cmppct_offense": float,
    "passing_yds_offense": float,
    "passing_avg_offense": float,
    "passing_yds_per_game_offense": float,
    "passing_longest_offense": float,
    "passing_td_offense": float,
    "passing_int_offense": float,
    "passing_sack_offense": float,
    "sack_yards_lost_offense": float,
    "passer_rating_offense": float
}

# maps the column names and types for offense rushing
offense_rushing_map = {
    "team": str,
    "games_offense": float,
    "rushing_att_offense": float,
    "rushing_yds_offense": float,
    "rushing_avg_offense": float,
    "rushing_yds_per_game_offense": float,
    "rushing_longest_offense": float,
    "rushing_td_offense": float,
    "rushing_fumbles_offense": float,
    "rushing_fumbles_lost_offense": float
}

# maps the column names and types for offense receiving
offense_receiving_map = {
    "team": str,
    "games_offense": float,
    "receiving_rec_offense": float,
    "receiving_yds_offense": float,
    "receiving_avg_offense": float,
    "receiving_yds_per_game_offense": float,
    "receiving_longest_offense": float,
    "receiving_td_offense": float,
    "receiving_fumbles_offense": float,
    "receiving_fumbles_lost_offense": float
}

# maps the column names and types for defense downs
offense_downs_map = {
    "team": str,
    "games_offense": float,
    "1st_total_offense": float,
    "1st_rush_offense": float,
    "1st_pass_offense": float,
    "1st_penalty_offense": float,
    "3rd_conv_offense": float,
    "3rd_att_offense": float,
    "3rd_pct_offense": float,
    "4th_conv_offense": float,
    "4th_att_offense": float,
    "4th_pct_offense": float,
    "offense_penalties": float,
    "offense_yds_lost": float
}
