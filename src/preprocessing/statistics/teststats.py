"""
Merges yearly team statistics from ESPN.
"""
import pandas as pd

from abc import ABC

from config.mapping import week_map
from src.preprocessing.preprocessing import Preprocessing
from src.loader.espn.teams import PassingDefense, RushingDefense, ReceivingDefense, DownsDefense
from src.loader.espn.teams import PassingOffense, RushingOffense, ReceivingOffense, DownsOffense


class Defense(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh=refresh)
        self.season = "REG"

        self.filename = f"defense_stats_{self.year}_{self.season}.csv"
        self.dir = f"../preprocessed/teamstats"

    def concat_data(self):
        """ Merges yearly team statistics from ESPN. """
        df = PassingDefense(self.year, self.season, self.refresh).get_data()
        df = pd.merge(df,
                      RushingDefense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      ReceivingDefense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      DownsDefense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])

        return df


class Offense(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh=refresh)
        self.season = "REG"

        self.filename = f"offense_stats_{self.year}_{self.season}.csv"
        self.dir = f"../preprocessed/teamstats"

    def concat_data(self):
        """ Merges yearly team statistics from ESPN. """
        df = PassingOffense(self.year, self.season, self.refresh).get_data()
        df = pd.merge(df,
                      RushingOffense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      ReceivingOffense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      DownsOffense(self.year, self.season, self.refresh).get_data(),
                      how="inner",
                      on=["team", "games", "year"])

        return df


def store_all():
    for year in week_map.keys():
        Defense(year, refresh=True).store_accumulated_data()
        Offense(year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()

