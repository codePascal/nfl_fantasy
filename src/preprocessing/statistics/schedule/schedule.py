import numpy as np
import pandas as pd


def get_schedule(year):
    """
    Gets the schedule for a given year and restructures it for single
    weeks and teams.

    :param year: year to get cleaned schedule
    :type year: int
    :return: cleaned schedule
    :rtype: pandas.DataFrame
    """
    # get the data
    df = pd.read_csv(f"../raw/schedules/schedule_{year}.csv")

    # drop the unnamed column
    df.drop(df.columns[0], axis=1, inplace=True)

    # clean up and return
    return clean_schedule(df)


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


if __name__ == "__main__":
    year = 2021
    df = get_schedule(year)

