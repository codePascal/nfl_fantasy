"""
Implements preprocessing of weekly data.

The weekly statistics are accumulated into one. Enables easier access
for a whole season.

Refreshing means, that it will, regardless if the file already
exists, accumulate the stats again. However, this does not mean that
the stats itself are refreshed.
"""
import os
import pandas as pd


class Preprocessing:
    def __init__(self, year, refresh=False):
        self.year = year
        self.refresh = refresh
        self.filename = str()
        self.dir = str()

    def concat_data(self):
        raise NotImplementedError

    def get_accumulated_data(self):
        """ Returns the accumulated weekly data. """
        if not os.path.exists(os.path.join(self.dir, self.filename)) or self.refresh:
            # accumulate data
            return self.concat_data()
        else:
            # load stored data
            return self.load_accumulated_data()

    def load_accumulated_data(self):
        """ Loads the stored csv file. """
        return pd.read_csv(os.path.join(self.dir, self.filename))

    def store_accumulated_data(self):
        """ Stores the accumulated weekly data. """
        if not os.path.exists(self.dir):
            os.makedirs(os.path.join(os.getcwd(), self.dir))
        self.get_accumulated_data().to_csv(os.path.join(self.dir, self.filename), index=False)

