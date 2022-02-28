""" Handles configuration for data from fantasy pros.

Glossary for help:
https://www.hometeamsonline.com/teams/popups/Glossary.asp?s=football
"""
# maps the column name and type for stats
stats_type = {
    "DST": {
        "rank": float,
        "player": str,
        "sacks": float,
        "ints": float,
        "frec": float,
        "ff": float,
        "defense_td": float,
        "sfty": float,
        "spc_td": float,
        "games": float,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "K": {
        "rank": float,
        "player": str,
        "fg": float,
        "fg_att": float,
        "fg_pct": float,
        "long": float,
        "1-19": float,
        "20-29": float,
        "30-39": float,
        "40-49": float,
        "50+": float,
        "XPT": float,
        "XPA": float,
        "games": float,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "QB": {
        "rank": float,
        "player": str,
        "passing_cmp": float,
        "passing_att": float,
        "passing_cmppct": float,
        "passing_yds": float,
        "passing_avg": float,
        "passing_td": float,
        "passing_int": float,
        "sacked": float,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "lst": float,
        "games": float,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "RB": {
        "rank": float,
        "player": str,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_avg": float,
        "rushing_lng": float,
        "rushing_20p": float,
        "rushing_td": float,
        "receiving_rec": float,
        "receiving_tgt": float,
        "receiving_yds": float,
        "receiving_avg": float,
        "receiving_td": float,
        "lst": float,
        "games": float,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "TE": {
        "rank": float,
        "player": str,
        "receiving_rec": float,
        "receiving_tgt": float,
        "receiving_yds": float,
        "receiving_avg": float,
        "receiving_long": float,
        "receiving_20p": float,
        "receiving_td": float,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "lst": float,
        "games": float,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "WR": {
        "rank": float,
        "player": str,
        "receiving_rec": float,
        "receiving_tgt": float,
        "receiving_yds": float,
        "receiving_avg": float,
        "receiving_lg": float,
        "receiving_20p": float,
        "receiving_td": float,
        "rushing_att": float,
        "rushing_yds": float,
        "rushing_td": float,
        "lst": float,
        "games": float,
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
    "games": float,
    "snaps": float,
    "snaps_per_game": float,
    "snaps_pct": float,
    "rush_pct": float,
    "tgt_pct": float,
    "touch_pct": float,
    "util_pct": float,
    "fantasy_points": float,
    "points_per_100_snaps": float
}

# maps the column name and type for projections
projections_type = {
    "DST": {
        "player": str,
        "sacks_proj": float,
        "ints_proj": float,
        "frec": float,
        "ff": float,
        "defense_td": float,
        "sfty": float,
        "pts_against": float,  # TODO verify
        "yds_against": float,  # TODO verify
        "fantasy_points": float
    },
    "K": {
        "player": str,
        "fg": float,
        "fg_att": float,
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
        "lst": float,
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
        "lst": float,
        "fantasy_points": float
    },
    "TE": {
        "player": str,
        "receiving_rec": float,
        "receiving_yds": float,
        "receiving_td": float,
        "lst": float,
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
        "lst": float,
        "fantasy_points": float
    }
}

# maps the column name and type for points allowed
# rank is float to deal with missing data
pa_type = {
    "team": str,
    "rank_qb": float,
    "pa_qb": float,
    "rank_rb": float,
    "pa_rb": float,
    "rank_wr": float,
    "pa_wr": float,
    "rank_te": float,
    "pa_te": float,
    "rank_k": float,
    "pa_k": float,
    "rank_dst": float,
    "pa_dst": float
}