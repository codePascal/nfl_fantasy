"""
Implement the data loading for latest projections for fantasy
players.

Currently, only the weekly projections for season 2021 are
available. Unfortunately, if a player has retired at the end of the
season, e.g. Tom Brady, its projections are not available anymore.

If this script is run, all projections for denoted year are stored.
"""
from abc import ABC

from config.mapping import projections_type, teams, week_map
from src.loader.loader import Loader


class Projections(Loader, ABC):
    def __init__(self, position, week):
        Loader.__init__(self)

        self.position = position
        self.week = week
        self.year = 2021

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/projections/{self.year}/{self.position.upper()}"
        self.url = f"https://www.fantasypros.com/nfl/projections/{self.position.lower()}.php?week={self.week}"

    def clean_data(self, df):
        """ Cleans data specifically for projections. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # assign better column names
        df.columns = list(projections_type[self.position].keys())

        # clean up general columns
        df["team"] = df.apply(get_team, axis=1)
        df["player"] = df["player"].apply(transform_name)

        # add position, week and year
        df["position"] = self.position
        df["week"] = self.week
        df["year"] = self.year

        # set column types
        return df.astype(projections_type[self.position])


def get_team(player):
    """ Extracts team from player entry. """
    for subname in player["player"].split():
        for team in teams:
            if team in subname:
                return team


def transform_name(name):
    """ Removes team from players name. """
    to_drop = ""
    for subname in name.split():
        for team in teams:
            if team in subname:
                to_drop = team
    return name.replace(to_drop, "")


def store_all():
    """ Stores all projections. """
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        for week in range(1, week_map[2021] + 1):
            Projections(position, week).store_data()


if __name__ == "__main__":
    store_all()

