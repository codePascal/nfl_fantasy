"""
Accumulates weekly stats and schedule for a season with the yearly
team stats for defense.

Running this script will store the accumulated statistics for a given
year range.
"""
import numpy as np
import pandas as pd

from abc import ABC

from config.mapping import week_map
from src.loader.fantasypros.schedule import Schedule
from src.preprocessing.preprocessing import Preprocessing
from src.preprocessing.statistics.stats import Stats
from src.preprocessing.statistics.teststats import Defense


class Statistics(Preprocessing, ABC):
    def __init__(self, position, year, refresh=False):
        Preprocessing.__init__(self, year, refresh)
        self.position = position
        self.year = year

        self.filename = f"statistics_{self.position}_{self.year}.csv"
        self.dir = f"../preprocessed/statistics/{self.year}"

    def concat_data(self):
        """ Concatenates weekly stats and schedule for given position
        with and opponent yearly stats.
        """
        season = Stats(self.position, self.year, refresh=self.refresh).get_accumulated_data()
        season.drop(["rank", "rost", "fantasy_points_per_game"], axis=1, inplace=True)

        schedule = Schedule(self.year).get_data()
        season = pd.merge(season, schedule, how="inner", on=["team", "week", "year"])
        season = season.loc[season["opponent"] != "BYE"]

        defense = Defense(self.year).get_accumulated_data()
        defense.drop(["games"], axis=1, inplace=True)
        defense.rename(columns={"team": "opponent"}, inplace=True)
        season = pd.merge(season, defense, how="inner", on=["opponent", "year"])

        return season


def store_all():
    """ Accumulates and stores the accumulated statistics. """
    for position in ["QB", "RB", "TE", "WR"]:
        for year in week_map.keys():
            Statistics(position, year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
