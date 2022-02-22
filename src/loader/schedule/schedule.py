"""
Implements the data handling for schedules presented in
https://www.fantasypros.com/nfl/schedule/grid.php. The schedules are
considered given as a grid.
"""
import os
import numpy as np
import pandas as pd

import src.loader.loader as loader


def clean_schedule(df):
    """
    Cleans up schedule and returns the team and its opponent per
    week. Includes if at home or away.

    :param df: schedule grid
    :type df: pandas.DataFrame
    :return: clean schedule
    :rtype: pandas.DataFrame
    """
    # drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

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


def fetch_schedule(year):
    """
    Fetches schedule from
    https://www.fantasypros.com/nfl/schedule/grid.php.

    :param year: year to fetch
    :type year: int
    :return: schedule
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_schedule(year))


def get_schedule(year):
    """
    Returns the schedule, either reads from stored file or fetches
    from webpage.

    :param year: year to fetch
    :type year: int
    :return: schedule
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/schedules/schedule_{year}.csv"):
        # fetch the schedule and clean
        df = fetch_schedule(year)
        return clean_schedule(df)
    else:
        # load cleaned schedule
        return pd.read_csv(f"../raw/schedules/schedule_{year}.csv")


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
    elif game.startswith("@"):
        return game[1:]
    elif game.startswith("vs"):
        return game[2:]


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


def get_url_schedule(year):
    return f"https://www.fantasypros.com/nfl/schedule/grid.php?year={year}"


def store_all_schedules(years):
    """
    Stores all schedules in a given year range.

    :param years: year range to fetch schedules
    :type years: tuple
    :return: None
    """
    for year in range(years[0], years[1] + 1):
        store_schedule(year)


def store_schedule(year):
    """
    Stores the schedule for a given year.

    :param year: year to fetch
    :type year: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/schedules")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/schedules"))
    get_schedule(year).to_csv(f"../raw/schedules/schedule_{year}.csv", index=False)


if __name__ == "__main__":
    store_all_schedules((2016, 2021))
