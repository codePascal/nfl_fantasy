"""
Implements the data loading for schedules from fantasy pros.

If this script is run, all schedules for denoted year range are
stored. Different to other loading implementations, this class
does not offer refreshing of the data since the data is altered in a
more complex way.
"""
import numpy as np
import pandas as pd

from abc import ABC

from config.mapping import week_map
from src.loader.fantasypros.fantasypros import FantasyProsLoader as Loader


class Schedule(Loader, ABC):
    def __init__(self, year, refresh=False):
        Loader.__init__(self, year, refresh)

        self.filename = f"schedule_{self.year}.csv"
        self.dir = f"../raw/schedules"
        self.url = f"https://www.fantasypros.com/nfl/schedule/grid.php?year={self.year}"

        # no refreshing available for schedules
        # TODO split into loading and preprocessing
        self.refresh = False

    def clean_data(self, df):
        """ Restructures schedule. """
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

        # add year
        schedule["year"] = self.year

        return schedule


def get_opponent(game):
    """ Returns the opponent of the game on the view of the team. """
    if game == "BYE":
        return game
    elif game.startswith("@"):
        return game[1:]
    elif game.startswith("vs"):
        return game[2:]


def get_location(game):
    """ Returns true if the team has a home game. """
    if game.startswith('@'):
        # away game
        return False
    elif game.startswith("vs"):
        # home game
        return True
    else:
        # bye week
        return np.nan


def store_all():
    """ Stores all schedules for given year range. """
    for year in week_map.keys():
        Schedule(year).store_data()


if __name__ == "__main__":
    store_all()

