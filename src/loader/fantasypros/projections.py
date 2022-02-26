"""
Implement the data loading for latest projections for fantasy
players.

Currently, only the weekly projections for season 2021 are
available. Unfortunately, if a player has retired at the end of the
season, e.g. Tom Brady, its projections are not available anymore.

If this script is run, all projections for denoted year are stored or
refreshed if already offline available.
"""
from abc import ABC

from config.fantasypros import projections_type
from config.mapping import team_map, teams, week_map
from src.loader.fantasypros.fantasypros import FantasyProsLoader as Loader


class Projections(Loader, ABC):
    def __init__(self, position, week, refresh=False):
        Loader.__init__(self, 2021, refresh)
        self.position = position
        self.week = week
        self.mapping = projections_type[self.position]
        self.to_add = {"position": self.position, "week": self.week, "year": self.year}

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/projections/{self.year}/{self.position.upper()}"
        self.url = f"https://www.fantasypros.com/nfl/projections/{self.position.lower()}.php?week={self.week}"

        self.original_columns_dict = {
            "DST": ['Player', 'SACK', 'INT', 'FR', 'FF', 'TD', 'SAFETY', 'PA', 'YDS AGN', 'FPTS'],
            "K": ['Player', 'FG', 'FGA', 'XPT', 'FPTS'],
            "QB": ['Player', 'ATT', 'CMP', 'YDS', 'TDS', 'INTS', 'ATT', 'YDS', 'TDS', 'FL', 'FPTS'],
            "RB": ['Player', 'ATT', 'YDS', 'TDS', 'REC', 'YDS', 'TDS', 'FL', 'FPTS'],
            "TE": ['Player', 'REC', 'YDS', 'TDS', 'FL', 'FPTS'],
            "WR": ['Player', 'REC', 'YDS', 'TDS', 'ATT', 'YDS', 'TDS', 'FL', 'FPTS']}
        self.original_columns = self.original_columns_dict[self.position]

    def clean_data(self, df):
        """ Cleans data specifically for projections. """
        df = self.map_columns(df)

        # clean up general columns
        df["team"] = df.apply(get_team, axis=1)
        df["player"] = df["player"].apply(transform_name)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set column types
        return df.astype(self.mapping)

    def restore_data(self, df):
        """ Restores data specifically for projections since some
        columns are altered during cleaning and should not be
        changed. """
        if not self.position == "DST":
            # restore specifically altered columns
            df["player"] = df["player"] + df["team"]

        # standard restoring
        df = df.loc[:, list(self.mapping.keys())[:len(self.original_columns)]]
        df.columns = self.original_columns

        return df


def get_team(player):
    """ Extracts team from player entry. """
    if player["player"] in team_map.keys():
        return team_map[player["player"]]
    else:
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
            Projections(position, week, refresh=True).store_data()


if __name__ == "__main__":
    store_all()
