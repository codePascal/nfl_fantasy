"""
Implements the data loading for weekly and yearly snapcount analysis.

Snap counts represent the total number of offensive plays a player
participated in. Higher snap counts and percentages indicate that
the player had more opportunities throughout his games.

Most recent years are available for that analysis. Currently, only
offensive players are available to fetch. These are drafted as single
players compared to the defenses that are drafted as one. Kickers are
not considered. All players are fetched that had more than 0 snaps.

If this script is run, all snapcounts for denoted year range are
stored.
"""
from abc import ABC

from config.mapping import snapcounts_type, week_map
from src.loader.loader import Loader

# TODO fix duplicated code fragments


class WeeklySnapcounts(Loader, ABC):
    def __init__(self, week, year):
        Loader.__init__(self)

        self.week = week
        self.year = year

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/weekly_snapcounts/{self.year}"
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={self.week}&snaps=0&range=week&year={self.year}"

    def clean_data(self, df):
        """ Cleans the data specifically for weekly snapcounts. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # rename column names in a more descriptive manner
        df.columns = list(snapcounts_type.keys())

        # transform snaps
        df["snaps"] = df["snaps"].apply(transform_snaps)

        # add week and year
        df["week"] = self.week
        df["year"] = self.year

        # set types
        return df.astype(snapcounts_type)


class YearlySnapcounts(Loader, ABC):
    def __init__(self, year):
        Loader.__init__(self)

        self.year = year

        self.filename = f"snapcounts_{self.year}.csv"
        self.dir = f"../raw/yearly_snapcounts"
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={self.year}&snaps=0&range=full"

    def clean_data(self, df):
        """ Cleans the data specifically for yearly snapcounts. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # rename column names in a more descriptive manner
        df.columns = list(snapcounts_type.keys())

        # transform snaps
        df["snaps"] = df["snaps"].apply(transform_snaps)

        # add the year
        df["year"] = self.year

        # set types
        return df.astype(snapcounts_type)


def transform_snaps(snaps):
    """ Removes comma in snap stats denoting a thousand. """
    if "," in str(snaps):
        return int(str(snaps).replace(",", ""))
    else:
        return snaps


def store_all():
    """ Stores all snapcounts for given year range. """
    years = (2010, 2021)
    for year in range(years[0], years[1] + 1):
        YearlySnapcounts(year).store_data()
        for week in range(1, week_map[year] + 1):
            WeeklySnapcounts(week, year).store_data()


if __name__ == "__main__":
    store_all()




