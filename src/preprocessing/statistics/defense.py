"""
Merges yearly team statistics from ESPN and Fantasy pros.
"""
import numpy as np
import pandas as pd

from abc import ABC

from src.preprocessing.preprocessing import Preprocessing
from src.loader.espn.teams import PassingDefense, RushingDefense, ReceivingDefense, DownsDefense
from src.loader.fantasypros.stats import YearlyStats


class MergeDefense(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh=refresh)
        self.season = "REG"
        self.position = "DST"

        self.filename = f"defense_stats_{self.year}_{self.season}.csv"
        self.dir = f"../preprocessed/teamstats"

    def concat_data(self):
        """ Merges yearly team statistics from ESPN with fantasy
        pros data. """
        df = YearlyStats(self.position, self.year, self.refresh).get_data()
        df.drop(["player", "rank", "position", "rost"], axis=1, inplace=True)
        df = pd.merge(df,
                      PassingDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year", "sacks", "ints"])
        df = pd.merge(df,
                      RushingDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      ReceivingDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      DownsDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])

        return df


class OffenseMerge(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh=refresh)
        self.season = "REG"
        self.position = "DST"

    def concat_data(self):
        """ Merges yearly team statistics from ESPN. """
        df = PassingDefense(self.year, self.season, self.refresh).get_data()
        df = pd.merge(df,
                      RushingDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      ReceivingDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])
        df = pd.merge(df,
                      DownsDefense(self.year, self.season, self.refresh).get_data(),
                      how="outer",
                      on=["team", "games", "year"])

        print(df.columns)

        return df

