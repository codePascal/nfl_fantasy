""" Implements the data loading for weekly and yearly stats. """
from abc import ABC

from config.mapping import stats_type
from src.loader.loader import Loader

# TODO fix duplicated code fragments
# TODO fix free agents with team during season


class WeeklyStats(Loader, ABC):
    def __init__(self, position, week, year):
        Loader.__init__(self)

        self.position = position
        self.week = week
        self.year = year

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/weekly_stats/{self.year}/{self.position.upper()}"
        self.url = f"https://www.fantasypros.com/nfl/stats/{self.position.lower()}.php?year={self.year}&week={self.week}&range=week"

    def clean_data(self, df):
        """ Cleans data specifically for weekly stats. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # assign better column names
        df.columns = list(stats_type[self.position].keys())

        # clean up general columns
        df["team"] = df.apply(get_team, axis=1)
        df["player"] = df["player"].apply(transform_name)
        df["rost"] = df["rost"].apply(transform_rost)

        # clean up specific columns
        if self.position == "DST":
            pass
        elif self.position == "K":
            pass
        elif self.position == "QB":
            df["passing_yds"] = df["passing_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
        elif self.position == "RB":
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
        elif self.position == "TE":
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
        elif self.position == "WR":
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)

        # add the position, week and year
        df["position"] = self.position
        df["week"] = self.week
        df["year"] = self.year

        # map the types of the columns
        return df.astype(stats_type[self.position])


class YearlyStats(Loader, ABC):
    def __init__(self, position, year):
        Loader.__init__(self)

        self.position = position
        self.year = year

        self.filename = f"{position.upper()}_{year}.csv"
        self.dir = f"../raw/yearly_stats/{year}/"
        self.url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"

    def clean_data(self, df):
        """ Cleans data specifically for yearly stats. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # assign better column names
        df.columns = list(stats_type[self.position].keys())

        # clean up general columns
        df["team"] = df.apply(get_team, axis=1)
        df["player"] = df["player"].apply(transform_name)
        df["rost"] = df["rost"].apply(transform_rost)

        # clean up specific columns
        if self.position == "DST":
            pass
        elif self.position == "K":
            pass
        elif self.position == "QB":
            df["passing_yds"] = df["passing_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
        elif self.position == "RB":
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
        elif self.position == "TE":
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
        elif self.position == "WR":
            df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
            df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)

        # add the position and the year
        df["position"] = self.position
        df["year"] = self.year

        # map the types of the columns
        return df.astype(stats_type[self.position])


def get_team(player):
    """ Extracts team from player entry. """
    return player["player"].split('(')[1].split(')')[0]


def transform_name( name):
    """ Removes team from players name. """
    return name.split('(')[0]


def transform_rost(rost):
    """ Removes the rost percentage sign. """
    return rost[:-1]


def transform_yards(yards):
    """ Removes comma in yards stats denoting a thousand. """
    if "," in str(yards):
        return int(str(yards).replace(",", ""))
    else:
        return yards
