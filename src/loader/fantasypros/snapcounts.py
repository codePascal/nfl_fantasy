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
stored or refreshed if already available offline.
"""
from abc import ABC

from config.fantasypros import snapcounts_type
from config.mapping import week_map
from src.loader.fantasypros.fantasypros import FantasyProsLoader as Loader


class Snapcounts(Loader, ABC):
    def __init__(self, year, refresh=False):
        Loader.__init__(self, year, refresh)
        self.mapping = snapcounts_type
        self.to_add = dict()

        self.original_columns = ['Player', 'Pos', 'Team', 'Games', 'Snaps', 'Snaps/Gm', 'Snap %', 'Rush %', 'Tgt %',
                                 'Touch %', 'Util %', 'Fantasy Pts', 'Pts/100 Snaps']


class WeeklySnapcounts(Snapcounts, ABC):
    def __init__(self, week, year, refresh=False):
        Snapcounts.__init__(self, year, refresh)
        self.week = week
        self.to_add = {"week": self.week, "year": self.year}

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/weekly_snapcounts/{self.year}"
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={self.week}&snaps=0&range=week&year={self.year}"


class YearlySnapcounts(Snapcounts, ABC):
    def __init__(self, year, refresh=False):
        Snapcounts.__init__(self, year, refresh)
        self.to_add = {"year": self.year}

        self.filename = f"snapcounts_{self.year}.csv"
        self.dir = f"../raw/yearly_snapcounts"
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={self.year}&snaps=0&range=full"


def store_all():
    """ Stores all snapcounts for given year range. """
    years = (2010, 2021)
    for year in range(years[0], years[1] + 1):
        YearlySnapcounts(year, refresh=True).store_data()
        for week in range(1, week_map[year] + 1):
            WeeklySnapcounts(week, year, refresh=True).store_data()


if __name__ == "__main__":
    store_all()



