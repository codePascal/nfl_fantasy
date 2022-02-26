"""
Accumulates all weekly snapcounts for a season into one.

Running this script will store all summaries for a denoted year
range.
"""

import pandas as pd

from abc import ABC

from config.mapping import week_map
from loader.fantasypros.snapcounts import WeeklySnapcounts as Loader
from src.preprocessing.preprocessing import Preprocessing


class Snapcounts(Preprocessing, ABC):
    def __init__(self, year):
        Preprocessing.__init__(self)

        self.year = year

        self.filename = f"snapcounts_summary_{self.year}.csv"
        self.dir = f"../preprocessed/snapcounts"

    def concat_data(self):
        """ Concatenates the weekly snapcounts into one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(week, self.year).get_data()])
        return df.reset_index(drop=True)


def store_all():
    """ Accumulates and stores all weekly snapcounts for a season. """
    years = (2010, 2021)
    for year in range(years[0], years[1] + 1):
        Snapcounts(year).store_accumulated_data()


if __name__ == "__main__":
    store_all()
