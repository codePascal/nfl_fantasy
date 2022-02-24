"""
Implements preprocessing of weekly data.

The weekly statistics are accumulated into one. Enables easier access
for a whole season.
"""
import os
import pandas as pd


class Preprocessing:
    def __init__(self):
        self.filename = "some_filename"
        self.dir = "some_dir"

    def concat_data(self):
        raise NotImplementedError

    def get_accumulated_data(self):
        """ Returns the accumulated weekly data. """
        if not os.path.exists(os.path.join(self.dir, self.filename)):
            return self.concat_data()
        else:
            return pd.read_csv(os.path.join(self.dir, self.filename))

    def store_accumulated_data(self):
        """ Stores the accumulated weekly data. """
        if not os.path.exists(self.dir):
            os.makedirs(os.path.join(os.getcwd(), self.dir))
        self.get_accumulated_data().to_csv(os.path.join(self.dir, self.filename), index=False)

