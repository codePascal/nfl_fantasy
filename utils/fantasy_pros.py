"""
Implements functions specifically designed for the data presented by
FANTASYPROS. It is assumed that the data is ordered regarding fantasy
points made during a season (FPTS).
"""

map_type_qb = {
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
    "misc_fl": int,
    "misc_g": int,
    "misc_fpts": float,
    "misc_fptsg": float,
    "misc_rost": float,
    "team": str
}

map_type_rb = {
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
    "misc_fl": int,
    "misc_g": int,
    "misc_fpts": float,
    "misc_fptsg": float,
    "misc_rost": float,
    "team": str
}

map_type_te = {
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
    "misc_fl": int,
    "misc_g": int,
    "misc_fpts": float,
    "misc_fptsg": float,
    "misc_rost": float,
    "team": str
}

map_type_wr = {
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
    "misc_fl": int,
    "misc_g": int,
    "misc_fpts": float,
    "misc_fptsg": float,
    "misc_rost": float,
    "team": str
}


def clean_stats_qb(df):
    """
    Cleans the QB statistics found here:
    https://www.fantasypros.com/nfl/stats/qb.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_qb.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["passing_yds"] = df["passing_yds"].apply(transform_yards)
    df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    df["misc_rost"] = df["misc_rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_qb)

    return df


def clean_stats_rb(df):
    """
    Cleans the RB statistics found here:
    https://www.fantasypros.com/nfl/stats/rb.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_rb.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
    df["misc_rost"] = df["misc_rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_rb)

    return df


def clean_stats_te(df):
    """
    Cleans the TE statistics found here:
    https://www.fantasypros.com/nfl/stats/te.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_te.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
    df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    df["misc_rost"] = df["misc_rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_te)

    return df


def clean_stats_wr(df):
    """
    Cleans the WR statistics found here:
    https://www.fantasypros.com/nfl/stats/wr.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_wr.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
    df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    df["misc_rost"] = df["misc_rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_wr)

    return df


def get_team(player):
    """
    Extracts team from player entry.

    :param player: Player stats
    :type player: pandas.Series
    :return: players team
    :rtype: str
    """
    return player["player"].split()[-1][1:-1]


def transform_name(name):
    """
    Removes team from players name.

    :param name: player name and team
    :type name: str
    :return: player name only
    :rtype: str
    """
    first_name = name.split()[0]
    last_name = name.split()[1]
    return " ".join([first_name, last_name])


def transform_yards(yards):
    """
    Removes comma in yards stats denoting thousand.

    :param yards: accomplished yards
    :type yards: str
    :return: accomplished yards in new format
    :rtype: int
    """
    if "," in str(yards):
        return int(str(yards).replace(",", ""))
    else:
        return yards


def transform_rost(rost):
    """
    Removes the rost percentage sign.

    :param rost: percentage of roosts in all leagues including %
    :type rost: str
    :return: percentage of roosts in all league excluding %
    :rtype: str
    """
    return rost[:-1]
