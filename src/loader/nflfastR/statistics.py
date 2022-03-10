"""
Implements play-by-play data loading and extracting from
https://github.com/nflverse/nflfastR-data. Data is fetched, extracted
and stored.

Requires the git repository cloned (e.g. git folder) besides this
repository.
"""
import os
import gzip
import shutil
import pandas as pd

from config.mapping import week_map

# TODO fix loading without cloning repository


class PlayByPlayData:
    def __init__(self, year):
        self.year = year
        self.dir = "../raw/play-by-play/"
        self.filename = f"play_by_play_{self.year}.csv"
        self.url = f"../../nflfastR-data/data/play_by_play_{self.year}.csv.gz"

    def extract_data(self):
        with gzip.open(self.url, 'rb') as f_in:
            with open(os.path.join(self.dir, self.filename), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def get_data(self):
        if not os.path.exists(os.path.join(self.dir, self.filename)):
            self.extract_data()
        return self.load_data()

    def load_data(self):
        df = pd.DataFrame()
        chunks = pd.read_csv(os.path.join(self.dir, self.filename), iterator=True, low_memory=False,
                             chunksize=10000)
        for chunk in chunks:
            chunk["year"] = self.year
            df = pd.concat([df, chunk])
        return df

    def store_data(self):
        if not os.path.exists(self.dir):
            os.makedirs(os.path.join(os.getcwd(), self.dir))
        self.get_data().to_csv(os.path.join(self.dir, self.filename), index=False)


if __name__ == "__main__":
    for year in week_map.keys():
        PlayByPlayData(year).store_data()
