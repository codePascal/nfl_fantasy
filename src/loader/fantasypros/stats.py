"""
Implements the data loading for weekly and yearly stats.

If this script is run, all stats for denoted year range are stored
or refreshed if already available offline.
"""
from abc import ABC

from config.fantasypros import stats_type
from config.mapping import week_map
from src.loader.fantasypros.fantasypros import FantasyProsLoader as Loader


# TODO fix free agents during season


class Stats(Loader, ABC):
    def __init__(self, position, year, refresh=False):
        Loader.__init__(self, year, refresh)
        self.position = position
        self.mapping = stats_type[self.position]
        self.to_add = dict()

        self.original_columns_dict = {
            "DST": ['Rank', 'Player', 'SACK', 'INT', 'FR', 'FF', 'DEF TD', 'SFTY', 'SPC TD', 'G', 'FPTS', 'FPTS/G',
                    'ROST'],
            "K": ['Rank', 'Player', 'FG', 'FGA', 'PCT', 'LG', '1-19', '20-29', '30-39', '40-49', '50+', 'XPT', 'XPA',
                  'G', 'FPTS', 'FPTS/G', 'ROST'],
            "QB": ['Rank', 'Player', 'CMP', 'ATT', 'PCT', 'YDS', 'Y/A', 'TD', 'INT', 'SACKS', 'ATT', 'YDS', 'TD', 'FL',
                   'G', 'FPTS', 'FPTS/G', 'ROST'],
            "RB": ['Rank', 'Player', 'ATT', 'YDS', 'Y/A', 'LG', '20+', 'TD', 'REC', 'TGT', 'YDS', 'Y/R', 'TD', 'FL',
                   'G', 'FPTS', 'FPTS/G', 'ROST'],
            "TE": ['Rank', 'Player', 'REC', 'TGT', 'YDS', 'Y/R', 'LG', '20+', 'TD', 'ATT', 'YDS', 'TD', 'FL', 'G',
                   'FPTS', 'FPTS/G', 'ROST'],
            "WR": ['Rank', 'Player', 'REC', 'TGT', 'YDS', 'Y/R', 'LG', '20+', 'TD', 'ATT', 'YDS', 'TD', 'FL', 'G',
                   'FPTS', 'FPTS/G', 'ROST']}
        self.original_columns = self.original_columns_dict[self.position]

    def clean_data(self, df):
        """ Cleans the stats' data. """
        # map column names
        df = self.map_columns(df)

        # transform team, player and rost
        df["team"] = df.apply(get_team, axis=1)
        df["player"] = df["player"].apply(transform_name)
        df["rost"] = df["rost"].apply(transform_rost)

        # clean up specific columns
        if self.position == "DST":
            pass
        elif self.position == "K":
            pass
        elif self.position == "QB":
            df["passing_yds"] = df["passing_yds"].apply(self.fix_thousands)
            df["rushing_yds"] = df["rushing_yds"].apply(self.fix_thousands)
        elif self.position == "RB":
            df["rushing_yds"] = df["rushing_yds"].apply(self.fix_thousands)
            df["receiving_yds"] = df["receiving_yds"].apply(self.fix_thousands)
        elif self.position == "TE":
            df["receiving_yds"] = df["receiving_yds"].apply(self.fix_thousands)
            df["rushing_yds"] = df["rushing_yds"].apply(self.fix_thousands)
        elif self.position == "WR":
            df["receiving_yds"] = df["receiving_yds"].apply(self.fix_thousands)
            df["rushing_yds"] = df["rushing_yds"].apply(self.fix_thousands)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        return df.astype(self.mapping)

    def restore_data(self, df):
        """ Restores data specifically for stats since some columns
        are altered during cleaning and should not be changed. """
        # restore specifically altered columns
        df["player"] = df["player"] + "(" + df["team"] + ")"

        # standard restoring
        df = df.loc[:, list(self.mapping.keys())[:len(self.original_columns)]]
        df.columns = self.original_columns

        return df


class WeeklyStats(Stats, ABC):
    def __init__(self, position, week, year, refresh=False):
        Stats.__init__(self, position, year, refresh)
        self.week = week
        self.to_add = {"position": self.position, "week": self.week, "year": self.year}

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/weekly_stats/{self.year}/{self.position.upper()}"
        self.url = f"https://www.fantasypros.com/nfl/stats/{self.position.lower()}.php?year={self.year}&week={self.week}&range=week"


class YearlyStats(Stats, ABC):
    def __init__(self, position, year, refresh=False):
        Stats.__init__(self, position, year, refresh)
        self.to_add = {"position": self.position, "year": self.year}

        self.filename = f"{position.upper()}_{year}.csv"
        self.dir = f"../raw/yearly_stats/{year}/"
        self.url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"


def get_team(player):
    """ Extracts team from player entry. """
    return player["player"].split('(')[1].split(')')[0]


def transform_name(name):
    """ Removes team from players name. """
    return name.split('(')[0]


def transform_rost(rost):
    """ Removes the rost percentage sign. """
    if "%" in str(rost):
        return str(rost).replace("%", "")
    else:
        return rost


def store_all():
    """ Stores all stats for given year range. """
    years = (2010, 2021)
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        for year in range(years[0], years[1] + 1):
            YearlyStats(position, year, refresh=True).store_data()
            for week in range(1, week_map[year] + 1):
                WeeklyStats(position, week, year, refresh=True).store_data()


if __name__ == "__main__":
    store_all()
