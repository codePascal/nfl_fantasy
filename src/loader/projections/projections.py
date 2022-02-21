"""
Implements data handling for latest projections presented in
https://www.fantasypros.com/nfl/projections/. These projections are
summarized per position and are available for each week.
"""
import os
import pandas as pd

import src.loader.loader as loader

# check which year is currently presented on webpage
YEAR = 2021

map_type = {
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


def clean_projections(df, position):
    """
    Cleans the projections and maps descriptive column names.

    :param df: projections for given position
    :type df: pandas.DataFrame
    :param position: position to clean
    :type position: str
    :return: cleaned projections
    :rtype: pandas.DataFrame
    """
    # drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # assign better column names
    df.columns = list(map_type[position].keys())

    # clean up general columns
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)

    # set column types
    return df.astype(map_type[position])


def fetch_projections(position, week):
    """
    Fetches the latest projections from
    https://www.fantasypros.com/nfl/projections/.

    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: latest weekly projections
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_projections(position, week))


def get_projections(position, week):
    """
    Returns the projections, either reads from stored file or fetches
    from webpage.

    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: latest weekly projections
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/projections/{YEAR}/{position}/week_{week}.csv"):
        # fetch and clean the data
        df = fetch_projections(position, week)
        df = clean_projections(df, position)
        df["week"] = week
        df["position"] = position
        return df
    else:
        # load the cleaned data
        return pd.read_csv(f"../raw/projections/{YEAR}/{position}/week_{week}.csv")


def get_team(player):
    """
    Extracts team from player entry.

    :param player: player stats
    :type player: pandas.Series
    :return: players team
    :rtype: str
    """
    # TODO Fixme
    last_team = player["player"].split()[-1]
    for i in range(1, len(last_team)):
        if last_team[i].isupper():
            return last_team[i:]


def get_url_projections(position, week):
    return f"https://www.fantasypros.com/nfl/projections/{position.lower()}.php?week={week}"


def store_all_projections():
    """ Stores all projections for given positions. """
    for position in ["QB", "WR", "RB", "TE", "DST", "K"]:
        for week in range(1, 18 + 1):
            store_projections(position, week)


def store_projections(position, week):
    """
    Stores the weekly projections for the position.

    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/projections/{YEAR}/{position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/projections/{YEAR}/{position.upper()}"))
    get_projections(position, week).to_csv(f"../raw/projections/{YEAR}/{position.upper()}/week_{week}.csv", index=False)


def transform_name(name):
    """
    Removes team from players name.

    :param name: player name and team
    :type name: str
    :return: player name only
    :rtype: str
    """
    # TODO Fixme
    return name.split('(')[0]


if __name__ == "__main__":
    pass
