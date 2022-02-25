"""
Holds general definitions for the whole project.
"""

# maps number of weeks per season
week_map = {
    2021: 18,
    2020: 17,
    2019: 17,
    2018: 17,
    2017: 17,
    2016: 17,
    2015: 17,
    2014: 17,
    2013: 17,
    2012: 17,
    2011: 17,
    2010: 17,
    2009: 17,
}

# maps team names to commonly used abbreviations
team_map = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAC",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}

# stores list of team abbreviations
teams = list(team_map.values())

# maps the column name and type for stats
stats_type = {
    "DST": {
        "rank": int,
        "player": str,
        "defense_sacks": int,
        "defense_ints": int,
        "fumble_recovery": int,
        "fumble_forced": int,
        "defense_td": int,
        "defense_safety": int,
        "defense_spc_td": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "K": {
        "rank": int,
        "player": str,
        "field_goal": int,
        "field_goal_att": int,
        "pct": float,
        "lg": int,
        "1-19": int,
        "20-29": int,
        "30-39": int,
        "40-49": int,
        "50+": int,
        "XPT": int,
        "XPA": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "QB": {
        "rank": int,
        "player": str,
        "passing_cmp": int,
        "passing_att": int,
        "passing_pct": float,
        "passing_yds": int,
        "passing_ya": float,
        "passing_td": int,
        "passing_int": int,
        "passing_sacks": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "RB": {
        "rank": int,
        "player": str,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_ya": float,
        "rushing_lg": int,
        "rushing_20p": int,
        "rushing_td": int,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "TE": {
        "rank": int,
        "player": str,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_lg": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "WR": {
        "rank": int,
        "player": str,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_lg": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    }
}

# maps the column name and type for snapcounts
snapcounts_type = {
    "player": str,
    "position": str,
    "team": str,
    "games": int,
    "snaps": int,
    "snaps_per_game": int,
    "snaps_percent": int,
    "rush_percent": int,
    "tgt_percent": int,
    "touch_percent": int,
    "util_percent": int,
    "fantasy_points": float,
    "points_per_100_snaps": float
}

# maps the column name and type for projections
projections_type = {
    "DST": {
        "player": str,
        "sacks": float,
        "defense_int": float,
        "fumble_recovery": float,
        "fumble_forced": float,
        "defense_td": float,
        "defense_safety": float,
        "pa": float,
        "yds_against": float,
        "fantasy_points": float
    },
    "K": {
        "player": str,
        "field_goal": float,
        "field_goal_att": float,
        "XPT": float,
        "fantasy_points": float
    },
    "QB": {
        "player": str,
        "passing_att": float,
        "passing_cmp": float,
        "passing_yds": float,
        "passing_td": float,
        "passing_int": float,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "fumbles_lost": float,
        "fantasy_points": float
    },
    "RB": {
        "player": str,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "receiving_rec": float,
        "receiving_yds": float,
        "receiving_td": float,
        "fumbles_lost": float,
        "fantasy_points": float
    },
    "TE": {
        "player": str,
        "receiving_rec": float,
        "receiving_yds": float,
        "receiving_td": float,
        "fumbles_lost": float,
        "fantasy_points": float
    },
    "WR": {
        "player": str,
        "receiving_rec": float,
        "receiving_yds": float,
        "receiving_td": float,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "fumbles_lost": float,
        "fantasy_points": float
    }
}

# maps the column name and type for points allowed
pa_type = {
    "team": str,
    "rank_qb": int,
    "pa_qb": float,
    "rank_rb": int,
    "pa_rb": float,
    "rank_wr": int,
    "pa_wr": float,
    "rank_te": int,
    "pa_te": float,
    "rank_k": int,
    "pa_k": float,
    "rank_dst": int,
    "pa_dst": float
}

# map team changes
team_changes_map = {
    "OAK": "LV",  # changed in 2020
    "SD": "LAC",  # changed in 2016
}
