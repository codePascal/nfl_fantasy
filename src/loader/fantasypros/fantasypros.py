"""
Implements the data loading. If the data is not available offline, it
is freshly fetched from https://www.fantasypros.com/nfl.

This is the base class for loading the data. The cleaning of the data
is implemented in the corresponding child classes. Make sure that the
data is available for the specified parameters.

The recorded fantasy points correspond to standard scoring. For other
scoring schemes, e.g. PPR or Half-PPR, the stats can be used to
compute points scored in that specific scheme.
"""
from abc import ABC

from src.loader.loader import Loader


class FantasyProsLoader(Loader, ABC):
    def __init__(self, year, refresh=False):
        Loader.__init__(self, refresh)
        self.year = year

    def restore_data(self, df):
        """ Restores dataframe back to original columns and column
        names """
        df = df.loc[:, list(self.mapping.keys())[:len(self.original_columns)]]
        df.columns = self.original_columns
        return df
