""" Handles configuration for data from ESPN.

Glossary for help:
https://www.hometeamsonline.com/teams/popups/Glossary.asp?s=football
"""
# maps the column names and types for defense passing
defense_passing_map = {
    "team": str,
    "games": float,
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
    "games": float,
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
    "games": float,
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
    "games": float,
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
    "games": float,
    "passing_cmp": float,
    "passing_att": float,
    "passing_cmppct": float,
    "passing_yds": float,
    "passing_avg": float,
    "passing_yds_per_game": float,
    "passing_longest": float,
    "passing_td": float,
    "passing_int": float,
    "passing_sack": float,
    "sack_yards_lost": float,
    "passer_rating": float
}

# maps the column names and types for offense rushing
offense_rushing_map = {
    "team": str,
    "games": float,
    "rushing_att": float,
    "rushing_yds": float,
    "rushing_avg": float,
    "rushing_yds_per_game": float,
    "rushing_longest": float,
    "rushing_td": float,
    "rushing_fumbles": float,
    "rushing_fumbles_lost": float
}

# maps the column names and types for offense receiving
offense_receiving_map = {
    "team": str,
    "games": float,
    "receiving_rec": float,
    "receiving_yds": float,
    "receiving_avg": float,
    "receiving_yds_per_game": float,
    "receiving_longest": float,
    "receiving_td": float,
    "receiving_fumbles": float,
    "receiving_fumbles_lost": float
}

# maps the column names and types for defense downs
offense_downs_map = {
    "team": str,
    "games": float,
    "1st_total": float,
    "1st_rush": float,
    "1st_pass": float,
    "1st_penalty": float,
    "3rd_conv": float,
    "3rd_att": float,
    "3rd_pct": float,
    "4th_conv": float,
    "4th_att": float,
    "4th_pct": float,
    "offense_penalties": float,
    "offense_yds_lost": float
}
