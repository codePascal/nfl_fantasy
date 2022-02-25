"""
Accumulates weekly stats for all positions for a season into one.

Running this script will store all summaries for a denoted year
range.
"""
import pandas as pd

from abc import ABC

from config.mapping import week_map
from src.loader.stats import WeeklyStats as Loader
from src.preprocessing.preprocessing import Preprocessing


class Stats(Preprocessing, ABC):
    def __init__(self, year):
        Preprocessing.__init__(self)

        self.year = year

        self.filename = f"stats_summary_{self.year}.csv"
        self.dir = f"../preprocessed/stats/"

    def concat_data(self):
        """ Concatenates the weekly stats for all positions into
        one. """
        df = pd.DataFrame()
        for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
            for week in range(1, week_map[self.year] + 1):
                df = pd.concat([df, Loader(position, week, self.year).get_data()])
        return df.reset_index(drop=True)


def store_all():
    """ Accumulates and stores all weekly stats for a season. """
    years = (2010, 2021)
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        for year in range(years[0], years[1] + 1):
            Stats(year).store_accumulated_data()


if __name__ == "__main__":
    store_all()
