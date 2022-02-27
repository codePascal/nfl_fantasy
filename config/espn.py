""" Handles configuration for data from ESPN.

Glossary for help:
https://www.hometeamsonline.com/teams/popups/Glossary.asp?s=football
"""
# maps the column names and types for defense passing
defense_passing_map = {
    "team": str,
    "games": int,
    "passing_cmp_allowed": int,
    "passing_att_allowed": int,
    "passing_cmppct_allowed": float,
    "passing_yds_allowed": int,
    "passing_avg_allowed": float,
    "passing_yds_allowed_per_game": float,
    "passing_longest_allowed": int,
    "passing_td_allowed": int,
    "ints": int,
    "sacks": int,
    "sack_yards_gained": int,
    "passer_rating": float
}

# maps the column names and types for defense rushing
defense_rushing_map = {
    "team": str,
    "games": int,
    "rushing_att_allowed": int,
    "rushing_yds_allowed": int,
    "rushing_avg_allowed": float,
    "rushing_yds_allowed_per_game": float,
    "rushing_longest_allowed": int,
    "rushing_td_allowed": int,
    "rushing_fumbles": int,
    "rushing_fumbles_lost": int
}

# maps the column names and types for defense receiving
defense_receiving_map = {
    "team": str,
    "games": int,
    "receiving_rec_allowed": int,
    "receiving_yds_allowed": int,
    "receiving_avg_allowed": float,
    "receiving_yds_allowed_per_game": float,
    "receiving_longest_allowed": int,
    "receiving_td_allowed": int,
    "receiving_fumbles": int,
    "receiving_fumbles_lost": int
}

# maps the column names and types for defense downs
defense_downs_map = {
    "team": str,
    "games": int,
    "1st_total_allowed": int,
    "1st_rush_allowed": int,
    "1st_pass_allowed": int,
    "1st_penalty_allowed": int,
    "3rd_conv_allowed": int,
    "3rd_att_allowed": int,
    "3rd_pct_allowed": float,
    "4th_conv_allowed": int,
    "4th_att_allowed": int,
    "4th_pct_allowed": float,
    "defense_penalties": int,
    "defense_yds_lost": int
}

# maps the column names and types for offense passing
offense_passing_map = {
    "team": str,
    "games": int,
    "passing_cmp": int,
    "passing_att": int,
    "passing_cmppct": float,
    "passing_yds": int,
    "passing_avg": float,
    "passing_yds_per_game": float,
    "passing_longest": int,
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
    "rushing_avg": float,
    "rushing_yds_per_game": float,
    "rushing_longest": int,
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
    "receiving_avg": float,
    "receiving_yds_per_game": float,
    "receiving_longest": int,
    "receiving_td": int,
    "receiving_fumbles": int,
    "receiving_fumbles_lost": int
}

# maps the column names and types for defense downs
offense_downs_map = {
    "team": str,
    "games": int,
    "1st_total": int,
    "1st_rush": int,
    "1st_pass": int,
    "1st_penalty": int,
    "3rd_conv": int,
    "3rd_att": int,
    "3rd_pct": float,
    "4th_conv": int,
    "4th_att": int,
    "4th_pct": float,
    "offense_penalties": int,
    "offense_yds_lost": int
}
