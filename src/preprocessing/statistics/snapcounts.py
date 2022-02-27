"""
Accumulates all weekly snapcounts for a season into one.

Refreshing means, that it will, regardless if the file already
exists, accumulate the stats again. However, this does not mean that
the stats itself are refreshed.

Running this script will store all summaries for a denoted year
range or refresh them if available offline.
"""
import pandas as pd

from abc import ABC

from config.mapping import week_map
from src.loader.fantasypros.snapcounts import WeeklySnapcounts as Loader
from src.preprocessing.preprocessing import Preprocessing


class Snapcounts(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh)
        self.filename = f"snapcounts_summary_{self.year}.csv"
        self.dir = f"../preprocessed/snapcounts"

    def concat_data(self):
        """ Concatenates the weekly snapcounts into one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(week, self.year, self.refresh).get_data()])
        df = df.loc[df["games"] == 1]
        return df.reset_index(drop=True)


def store_all():
    """ Accumulates and stores all weekly snapcounts for a season. """
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        Snapcounts(year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
