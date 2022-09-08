"""
Accumulates all weekly projections into one.

Refreshing means, that it will, regardless if the file already
exists, accumulate the stats again. However, this does not mean that
the stats itself are refreshed.

Running this script will store all summaries for the year 2021 or
refresh them if available offline.
"""
import pandas as pd

from abc import ABC

from src.config.mapping import week_map
from src.loader.fantasypros.projections import Projections as Loader
from src.preprocessing.preprocessing import Preprocessing


class Projections(Preprocessing, ABC):
    def __init__(self, position, refresh=False):
        Preprocessing.__init__(self, 2021, refresh)
        self.position = position
        self.filename = f"projections_summary_{self.position.upper()}_{self.year}.csv"
        self.dir = f"../preprocessed/projections/{self.year}"

    def concat_data(self):
        """ Concatenates the weekly projections into one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(self.position, week, self.refresh).get_data()])
        return df.reset_index(drop=True)


def store_all():
    """ Accumulates and stores the weekly projections. """
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        Projections(position, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
