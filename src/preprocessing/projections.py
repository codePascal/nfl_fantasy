"""
Accumulates all weekly projections into one.

Running this script will store all summaries for the recent
data.
"""
import pandas as pd

from abc import ABC

from config.mapping import week_map
from loader.fantasypros.projections import Projections as Loader
from src.preprocessing.preprocessing import Preprocessing


class Projections(Preprocessing, ABC):
    def __init__(self, position):
        Preprocessing.__init__(self)

        self.position = position
        self.year = 2021

        self.filename = f"projections_summary_{self.position.upper()}_{self.year}.csv"
        self.dir = f"../preprocessed/projections"

    def concat_data(self):
        """ Concatenates the weekly projections into one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(self.position, week).get_data()])
        return df.reset_index(drop=True)


def store_all():
    """ Accumulates and stores the weekly projections. """
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        Projections(position).store_accumulated_data()


if __name__ == "__main__":
    store_all()
