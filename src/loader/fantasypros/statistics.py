"""
Implements the data handling for data fetched from
https://www.fantasypros.com/nfl. If the data is not available
offline, it is freshly fetched from the website.

The recorded fantasy points correspond to standard scoring. For other
scoring schemes, e.g. PPR or Half-PPR, the stats can be used to
calculate points scored in that specific scheme.
"""
import bs4
import pandas as pd
import requests
import numpy as np
import sys

from abc import ABC

from config.mapping import team_map, teams
from config.fantasypros import projections_type, pa_type, snapcounts_type, stats_type

from src.loader.loader import Loader
from src.loader.ffdp.ffdp import TeamsLoader


class FantasyProsLoader(Loader, ABC):
    def __init__(self, year, refresh=False):
        Loader.__init__(self, refresh)
        self.year = year

    def get_html_content(self):
        """ Reads HTML content and returns data table. """
        # get HTML config
        print("Fetching from", self.url)
        req = requests.get(self.url)

        # observe HTML output -> https://webformatter.com/html
        # print(req.text)

        # get table raw
        soup = bs4.BeautifulSoup(req.content, "html.parser")
        table = soup.find(id="data")
        data = self.get_table_data(table)

        # return as pandas DataFrame
        return pd.DataFrame(data[1:], columns=data[0])


class Schedule(FantasyProsLoader, ABC):
    def __init__(self, year, refresh=False):
        FantasyProsLoader.__init__(self, year, refresh)

        self.filename = f"schedule_{self.year}.csv"
        self.dir = f"../raw/schedules"
        self.url = f"https://www.fantasypros.com/nfl/schedule/grid.php?year={self.year}"

        # no refreshing available for schedules
        # TODO split into loading and preprocessing
        self.refresh = False

    def clean_data(self, df):
        """ Restructures schedule. """
        # drop unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # prepare schedule first
        df.columns = ["team"] + [str(i) for i in range(1, df.shape[1])]
        df.set_index("team", drop=True, inplace=True)
        df.dropna(inplace=True)

        # extract game information
        schedule = pd.DataFrame(columns=["team", "opponent", "week", "home"])
        for i, games in df.iterrows():
            for j, game in enumerate(games):
                schedule = pd.concat([schedule, pd.DataFrame({"team": [i],
                                                              "opponent": [self.get_opponent(game)],
                                                              "week": [j + 1],
                                                              "home": [self.get_location(game)]})],
                                     ignore_index=True)

        # add year
        schedule["year"] = self.year

        return schedule

    @staticmethod
    def get_opponent(game):
        """ Returns the opponent of the game on the view of the team. """
        if game == "BYE" or game == '-':
            return "BYE"
        elif game.startswith("@"):
            return game[1:]
        elif game.startswith("vs"):
            return game[2:]

    @staticmethod
    def get_location(game):
        """ Returns true if the team has a home game. """
        if game.startswith('@'):
            # away game
            return False
        elif game.startswith("vs"):
            # home game
            return True
        else:
            # bye week
            return np.nan


class Projections(FantasyProsLoader, ABC):
    """
    Implement the data loading for latest projections for fantasy
    players from fantasy pros.

    Currently, only the weekly projections for season 2021 are
    available. Unfortunately, if a player has retired at the end of
    the season, e.g. Tom Brady, its projections are not available
    anymore.
    """
    def __init__(self, position, week, refresh=False):
        FantasyProsLoader.__init__(self, 2021, refresh)
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
        df["team"] = df.apply(self.get_team, axis=1)
        df["player"] = df["player"].apply(self.transform_name)

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
        df = df.iloc[:, :len(self.original_columns)]
        df.columns = self.original_columns

        return df

    @staticmethod
    def get_team(player):
        """ Extracts team from player entry. """
        if player["player"] in team_map.keys():
            return team_map[player["player"]]
        else:
            for subname in player["player"].split():
                for team in teams:
                    if team in subname:
                        return team

    @staticmethod
    def transform_name(name):
        """ Removes team from players name. """
        to_drop = ""
        for subname in name.split():
            for team in teams:
                if team in subname:
                    to_drop = team
        return name.replace(to_drop, "")


class PointsAllowed(FantasyProsLoader, ABC):
    """
    Implements the data loading for points allowed from fantasypros.

    Fantasy Points Allowed is a metric that indicates how good or bad
    each NFL defense is at limiting fantasy production to their
    opponents. Teams that rank in the top 8 surrender the most fantasy
    points. They represent easy matchups that fantasy owners should
    target. On the flip side, teams that rank in the bottom 8 are
    difficult matchups that fantasy owners should take into
    consideration for start/sit decisions.

    Most recent years (back to 2015) are available. However, in some
    cases, e.g. Las Vegas Raiders, the name of the team has changed.
    Since team names are kept up to date, the points allowed for such a
    team are not available. Further, the points of the previous name are
    not available too.
    """
    def __init__(self, year, refresh=False):
        FantasyProsLoader.__init__(self, year, refresh)
        self.mapping = pa_type
        self.to_add = {"year": self.year}

        self.filename = f"points_allowed_{self.year}.csv"
        self.dir = f"../raw/points_allowed"
        self.url = f"https://www.fantasypros.com/nfl/points-allowed.php?year={self.year}"

        # TODO add restoring
        self.refresh = False

    def clean_data(self, df):
        """ Cleans data specifically for points allowed. """
        # back in 2015, points against only features offense positions
        self.mapping = dict([item for item in self.mapping.items()][:df.shape[1]])
        df = self.map_columns(df)

        # assign team shortcut
        df["team"] = df["team"].apply(self.add_team_shortcut)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # ranks might contain an empty string
        for i, column in enumerate(df.columns.to_list()):
            if "rank_" in column:
                for j in range(32):
                    if df.iloc[j, i] == "":
                        df.iloc[j, i] = np.nan

        # set column types
        return df.astype(self.mapping)

    def get_html_content(self):
        """ Reads HTML content and returns data table. """
        # get HTML config
        print("Fetching from", self.url)
        req = requests.get(self.url)

        # observe HTML output -> https://webformatter.com/html
        # print(req.text)

        # get table raw
        soup = bs4.BeautifulSoup(req.content, "html.parser")
        table = soup.find(id="data")
        data = self.get_table_data(table)

        # in that specific case, the content of the table is within one single list
        data_mod = list()
        data_mod.append(data[0])
        for i in range(0, len(data[1]), len(data[0])):
            data_mod.append(data[1][i:i+len(data[0])])

        # return as pandas DataFrame
        return pd.DataFrame(data_mod[1:], columns=data[0])

    @staticmethod
    def add_team_shortcut(team):
        """ Replaces team name with commonly used shortcut. """
        return team_map[team]


class Snapcounts(FantasyProsLoader, ABC):
    """
    Implements the data loading for weekly and yearly snapcount analysis
    from fantasy pros.

    Snap counts represent the total number of offensive plays a player
    participated in. Higher snap counts and percentages indicate that
    the player had more opportunities throughout his games.

    Most recent years are available for that analysis. Currently, only
    offensive players are available to fetch. These are drafted as single
    players compared to the defenses that are drafted as one. Kickers are
    not considered. All players are fetched that had more than 0 snaps.

    Snapcounts are only available back to season 2016.
    """
    def __init__(self, year, refresh=False):
        FantasyProsLoader.__init__(self, year, refresh)

        # check year
        if self.year < 2016:
            sys.exit("Snapcounts are only available for seasons 2016 and onwards.")

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


class Stats(FantasyProsLoader, ABC):
    """
    Implements the data loading for weekly and yearly stats from
    fantasy pros.

    A word on teams: somehow the statistics are updated recursively. E.g.
    if a player retired, all stats of that player will have (FA).
    A workaround is used to overcome this and use other stats to update
    the team accordingly.
    """
    def __init__(self, position, year, refresh=False):
        FantasyProsLoader.__init__(self, year, refresh)
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

        # TODO fix kicker and defense team assignment
        if self.position == "K" or self.position == "DST":
            raise NotImplementedError

    def restore_data(self, df):
        """ Restores data specifically for stats since some columns
        are altered during cleaning and should not be changed. """
        # restore specifically altered columns
        df["player"] = df["player"] + "(" + df["team"] + ")"

        # standard restoring
        df = df.iloc[:, :len(self.original_columns)]
        df.columns = self.original_columns

        return df

    @staticmethod
    def get_team(player):
        """ Extracts team from player entry. """
        return player["player"].split('(')[1].split(')')[0]

    @staticmethod
    def transform_name(name):
        """ Removes team from players name. """
        return name.split('(')[0]

    @staticmethod
    def transform_rost(rost):
        """ Removes the rost percentage sign. """
        if "%" in str(rost):
            return str(rost).replace("%", "")
        else:
            return rost


class WeeklyStats(Stats, ABC):
    def __init__(self, position, week, year, refresh=False):
        Stats.__init__(self, position, year, refresh)
        self.week = week
        self.to_add = {"position": self.position, "week": self.week, "year": self.year}

        self.filename = f"week_{self.week}.csv"
        self.dir = f"../raw/weekly_stats/{self.year}/{self.position.upper()}"
        self.url = f"https://www.fantasypros.com/nfl/stats/{self.position.lower()}.php?year={self.year}&week={self.week}&range=week"

    def clean_data(self, df):
        """ Cleans the stats' data. """
        # map column names
        df = self.map_columns(df)

        # fix a thousand notations
        for column in df.columns.to_list():
            df[column] = df[column].apply(self.fix_thousands)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # transform team, player and rost
        df["player"] = df["player"].apply(self.transform_name)
        df["rost"] = df["rost"].apply(self.transform_rost)

        # load player info and merge
        teams = TeamsLoader(self.year).get_data()
        teams = teams.loc[teams["position"] == self.position, ["player", "team", "week", "year"]]
        df = pd.merge(df, teams, how="inner", on=["player", "week", "year"])

        return df.astype(self.mapping)


class YearlyStats(Stats, ABC):
    def __init__(self, position, year, refresh=False):
        Stats.__init__(self, position, year, refresh)
        self.to_add = {"position": self.position, "year": self.year}

        self.filename = f"{position.upper()}_{year}.csv"
        self.dir = f"../raw/yearly_stats/{year}/"
        self.url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"

    def clean_data(self, df):
        """ Cleans the stats' data. """
        # map column names
        df = self.map_columns(df)

        # fix a thousand notations
        for column in df.columns.to_list():
            df[column] = df[column].apply(self.fix_thousands)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # transform team, player and rost
        df["player"] = df["player"].apply(self.transform_name)
        df["rost"] = df["rost"].apply(self.transform_rost)

        # TODO fix team assignment -> what to do if player changed his team during the season
        df["team"] = "team"

        return df.astype(self.mapping)
