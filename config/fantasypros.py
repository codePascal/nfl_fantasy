""" Handles configuration for data from fantasy pros.

Glossary for help:
https://www.hometeamsonline.com/teams/popups/Glossary.asp?s=football
"""
# maps the column name and type for stats
stats_type = {
    "DST": {
        "rank": int,
        "player": str,
        "sacks": int,
        "ints": int,
        "frec": int,
        "ff": int,
        "defense_td": int,
        "sfty": int,
        "spc_td": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "K": {
        "rank": int,
        "player": str,
        "fg": int,
        "fg_att": int,
        "fg_pct": float,
        "long": int,
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
        "passing_cmppct": float,
        "passing_yds": int,
        "passing_avg": float,
        "passing_td": int,
        "passing_int": int,
        "sacked": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "lst": int,
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
        "rushing_avg": float,
        "rushing_lng": int,
        "rushing_20p": int,
        "rushing_td": int,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_avg": float,
        "receiving_td": int,
        "lst": int,
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
        "receiving_avg": float,
        "receiving_long": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "lst": int,
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
        "receiving_avg": float,
        "receiving_lg": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "lst": int,
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
    "snaps_pct": int,
    "rush_pct": int,
    "tgt_pct": int,
    "touch_pct": int,
    "util_pct": int,
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