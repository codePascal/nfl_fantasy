"""
Implements functions specifically designed for the data presented by
FANTASYPROS. It is assumed that the data is ordered regarding fantasy
points made during a season (FPTS).
"""
import numpy as np
import pandas as pd

map_type_dst = {
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
    "rost": float,
    "team": str
}

map_type_k = {
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
    "rost": float,
    "team": str
}

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
    "fumbles_lost": int,
    "games": int,
    "fantasy_points": float,
    "fantasy_points_per_game": float,
    "rost": float,
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
    "fumbles_lost": int,
    "games": int,
    "fantasy_points": float,
    "fantasy_points_per_game": float,
    "rost": float,
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
    "fumbles_lost": int,
    "games": int,
    "fantasy_points": float,
    "fantasy_points_per_game": float,
    "rost": float,
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
    "fumbles_lost": int,
    "games": int,
    "fantasy_points": float,
    "fantasy_points_per_game": float,
    "rost": float,
    "team": str
}

map_type_snapcount = {
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


def concat_weekly_offensive_stats(year, weeks):
    """
    Concatenates weekly offensive stats. Takes only players into
    account that have played that week.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    weekly_stats = pd.DataFrame()

    for position in ["QB", "RB", "WR", "TE", "K"]:
        for week in range(1, weeks + 1):
            df = pd.read_csv(f"../data/weekly_stats/{year}/{position}/week_{week}.csv")
            df = clean_stats(df, position)
            df["week"] = week
            df["position"] = position

            # rank is not required
            df.drop("rank", axis=1, inplace=True)

            weekly_stats = pd.concat([weekly_stats, df])

    weekly_stats.reset_index(drop=True, inplace=True)
    return weekly_stats


def concat_weekly_snapcounts(year, weeks):
    """
    Concatenates weekly snapcount stats.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized snapcount analysis for the season
    :rtype: pandas.DataFrame
    """
    snapcount_stats = pd.DataFrame()

    for week in range(1, weeks + 1):
        df = pd.read_csv(f"../data/weekly_snapcounts/{year}/week_{week}.csv")
        df = clean_snapcount_analysis(df)
        df["week"] = week
        snapcount_stats = pd.concat([snapcount_stats, df])

    snapcount_stats.reset_index(drop=True, inplace=True)
    return snapcount_stats


def clean_stats(df, position):
    """
    Clean the stats found here:
    https://www.fantasypros.com/nfl/stats/

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :param position: position to clean
    :type position: str
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # drop unnamed column
    df.drop(df.columns[0], axis=1, inplace=True)

    # clean up depending on position
    if position == "DST":
        return clean_stats_dst(df)
    elif position == "K":
        return clean_stats_k(df)
    elif position == "QB":
        return clean_stats_qb(df)
    elif position == "RB":
        return clean_stats_rb(df)
    elif position == "TE":
        return clean_stats_te(df)
    elif position == "WR":
        return clean_stats_wr(df)


def clean_stats_dst(df):
    """
    Cleans the defensive statistics found here:
    https://www.fantasypros.com/nfl/stats/dst.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_dst.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["rost"] = df["rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_dst)

    return df


def clean_stats_k(df):
    """
    Cleans the kicker statistics found here:
    https://www.fantasypros.com/nfl/stats/k.php

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type_k.keys())[:-1]

    # transform column entries
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["rost"] = df["rost"].apply(transform_rost)

    # set types
    df = df.astype(map_type_k)

    return df


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
    df["rost"] = df["rost"].apply(transform_rost)

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
    df["rost"] = df["rost"].apply(transform_rost)

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
    df["rost"] = df["rost"].apply(transform_rost)

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
    df["rost"] = df["rost"].apply(transform_rost)

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
    return player["player"].split('(')[1].split(')')[0]


def transform_name(name):
    """
    Removes team from players name.

    :param name: player name and team
    :type name: str
    :return: player name only
    :rtype: str
    """
    return name.split('(')[0]


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


def clean_schedule(df):
    """
    Cleans up schedule and returns the team and its opponent per
    week. Includes if at home or away.

    :param df: schedule as read from csv
    :type df: pandas.DataFrame
    :return: clean schedule
    :rtype: pandas.DataFrame
    """
    # prepare schedule first
    df.columns = ["team"] + [str(i) for i in range(1, df.shape[1])]
    df.set_index("team", drop=True, inplace=True)
    df.dropna(inplace=True)

    # extract game information
    schedule = pd.DataFrame(columns=["team", "opponent", "week", "home"])
    for i, games in df.iterrows():
        for j, game in enumerate(games):
            schedule = pd.concat([schedule, pd.DataFrame({"team": [i],
                                                          "opponent": [get_opponent(game)],
                                                          "week": [j + 1],
                                                          "home": [get_location(game)]})],
                                 ignore_index=True)

    return schedule


def get_opponent(game):
    """
    Returns the opponent of the game on the view of the team. If the
    team has bye week, returns BYE.

    :param game: information about location and opponent
    :type game: str
    :return: opponent or BYE
    :rtype: str
    """
    if game == "BYE":
        return game
    return game.split()[1]


def get_location(game):
    """
    Returns the location of the game on the view of the team. If the
    team has bye week, returns nan.

    :param game: information about location and opponent
    :type game: str
    :return: location, home = True, away = False
    :rtype: bool
    """
    if game.startswith('@'):
        return False
    elif game.startswith("vs"):
        return True
    else:
        return np.nan


def clean_snapcount_analysis(df):
    """
    Cleans up snapcount analysis.

    :param df: analysis as read from csv
    :type df: pandas.DataFrame
    :return: cleaned snapcount analysis
    :rtype: pandas.DataFrame
    """
    # drop unnamed column
    df.drop(df.columns[0], axis=1, inplace=True)

    # rename column names in a more descriptive manner
    df.columns = list(map_type_snapcount.keys())

    # set types
    df = df.astype(map_type_snapcount)

    return df
