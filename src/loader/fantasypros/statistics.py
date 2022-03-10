"""
Implements the data handling for data fetched from
https://www.fantasypros.com/nfl. If the data is not available
offline, it is freshly fetched from the website.

The recorded fantasy points correspond to standard scoring. For other
scoring schemes, e.g. PPR or Half-PPR, the stats can be used to
calculate points scored in that specific scheme.
"""
import pandas as pd
import numpy as np
import sys

from abc import ABC

from config.mapping import team_map, teams, week_map
from config.fantasypros import projections_type, pa_type, snapcounts_type, stats_type

from src.loader.loader import Loader
from src.loader.fantasydatapros.statistics import TeamsLoader


class FantasyProsLoader(Loader, ABC):
    def __init__(self, year):
        Loader.__init__(self)
        self.year = year


class Schedule(FantasyProsLoader, ABC):
    def __init__(self, year):
        FantasyProsLoader.__init__(self, year)
        self.dir = f"../raw/schedules"
        self.filename = f"schedule_{self.year}.csv"
        self.to_add = {"year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/schedule/grid.php?year={self.year}"

    def clean_data(self, df):
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

        schedule = self.add_columns(schedule)
        return schedule

    @staticmethod
    def get_location(game):
        if game.startswith('@'):
            return False
        elif game.startswith("vs"):
            return True
        else:
            return np.nan

    @staticmethod
    def get_opponent(game):
        if game == "BYE" or game == '-':
            return "BYE"
        elif game.startswith("@"):
            return game[1:]
        elif game.startswith("vs"):
            return game[2:]


class Projections(FantasyProsLoader, ABC):
    """
    Implement the data loading for latest projections for fantasy
    players from fantasy pros.

    Currently, only the weekly projections for season 2021 are
    available. Unfortunately, if a player has retired at the end of
    the season, e.g. Tom Brady, its projections are not available
    anymore.
    """

    def __init__(self, position, week):
        FantasyProsLoader.__init__(self, 2021)
        self.position = position
        self.week = week

        self.dir = f"../raw/projections/{self.year}/{self.position.upper()}"
        self.filename = f"week_{self.week}.csv"
        self.mapping = projections_type[self.position]
        self.to_add = {"position": self.position, "week": self.week, "year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/projections/{self.position.lower()}.php?week={self.week}"

    def fix_columns(self, df):
        df["team"] = df.apply(self.get_team, axis=1)
        df["player"] = df["player"].apply(self.transform_name)
        return df

    @staticmethod
    def get_team(player):
        if player["player"] in team_map.keys():
            return team_map[player["player"]]
        else:
            for subname in player["player"].split():
                for team in teams:
                    if team in subname:
                        return team

    @staticmethod
    def transform_name(name):
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

    def __init__(self, year):
        FantasyProsLoader.__init__(self, year)
        self.dir = f"../raw/points_allowed"
        self.filename = f"points_allowed_{self.year}.csv"
        self.mapping = pa_type
        self.to_add = {"year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/points-allowed.php?year={self.year}"

    def map_columns(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # back in 2015, points against only features offense positions
        self.mapping = dict([item for item in self.mapping.items()][:df.shape[1]])
        df.columns = list(self.mapping.keys())
        return df

    def fix_columns(self, df):
        df["team"] = df["team"].apply(self.add_team_abbreviation)
        for i, column in enumerate(df.columns.to_list()):
            if "rank_" in column:
                for j in range(32):
                    if df.iloc[j, i] == "":
                        df.iloc[j, i] = np.nan
        return df

    @staticmethod
    def transform_to_frame(data):
        data_mod = list()
        data_mod.append(data[0])
        for i in range(0, len(data[1]), len(data[0])):
            data_mod.append(data[1][i:i + len(data[0])])
        return pd.DataFrame(data_mod[1:], columns=data[0])

    @staticmethod
    def add_team_abbreviation(team):
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

    def __init__(self, year):
        FantasyProsLoader.__init__(self, year)
        if self.year < 2016:
            sys.exit("Snapcounts are only available for seasons 2016 and onwards.")
        self.mapping = snapcounts_type
        self.to_add = dict()


class WeeklySnapcounts(Snapcounts, ABC):
    def __init__(self, week, year):
        Snapcounts.__init__(self, year)
        self.week = week

        self.dir = f"../raw/weekly_snapcounts/{self.year}"
        self.filename = f"week_{self.week}.csv"
        self.to_add = {"week": self.week, "year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={self.week}&snaps=0&range=week&year={self.year}"


class YearlySnapcounts(Snapcounts, ABC):
    def __init__(self, year):
        Snapcounts.__init__(self, year)
        self.dir = f"../raw/yearly_snapcounts"
        self.filename = f"snapcounts_{self.year}.csv"
        self.to_add = {"year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={self.year}&snaps=0&range=full"


class Stats(FantasyProsLoader, ABC):
    """
    Implements the data loading for weekly and yearly stats from
    fantasy pros.

    A word on teams: somehow the statistics are updated recursively. E.g.
    if a player retired, all stats of that player will have (FA) as team.
    A workaround is used to overcome this and use other stats to update
    the team accordingly.
    """

    def __init__(self, position, year):
        FantasyProsLoader.__init__(self, year)
        self.position = position

        self.mapping = stats_type[self.position]
        self.to_add = dict()

        # TODO fix kicker and defense team assignment
        if self.position == "K" or self.position == "DST":
            raise NotImplementedError

    @staticmethod
    def get_team(player):
        return player["player"].split('(')[1].split(')')[0]

    @staticmethod
    def transform_name(name):
        return name.split('(')[0]

    @staticmethod
    def transform_rost(rost):
        if "%" in str(rost):
            return str(rost).replace("%", "")
        else:
            return rost


class WeeklyStats(Stats, ABC):
    def __init__(self, position, week, year):
        Stats.__init__(self, position, year)
        self.week = week

        self.dir = f"../raw/weekly_stats/{self.year}/{self.position.upper()}"
        self.filename = f"week_{self.week}.csv"
        self.to_add = {"position": self.position, "week": self.week, "year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/stats/{self.position.lower()}.php?year={self.year}&week={self.week}&range=week"

    def fix_columns(self, df):
        df["player"] = df["player"].apply(self.transform_name)
        df["rost"] = df["rost"].apply(self.transform_rost)
        team_assignment = TeamsLoader(self.year).get_data()
        team_assignment = team_assignment.loc[
            team_assignment["position"] == self.position, ["player", "team", "week", "year"]]
        df = pd.merge(df, team_assignment, how="inner", on=["player", "week", "year"])
        return df


class YearlyStats(Stats, ABC):
    def __init__(self, position, year):
        Stats.__init__(self, position, year)
        self.dir = f"../raw/yearly_stats/{year}/"
        self.filename = f"{position.upper()}_{year}.csv"
        self.to_add = {"position": self.position, "year": self.year}
        self.url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"

    def fix_columns(self, df):
        df["player"] = df["player"].apply(self.transform_name)
        df["rost"] = df["rost"].apply(self.transform_rost)
        # TODO fix team assignment -> what to do if player changed his team during the season
        df["team"] = "team"

        return df


def store_all():
    for position in ["QB", "RB", "TE", "WR"]:
        for year in week_map.keys():
            YearlyStats(position, year).store_data()
            for week in range(1, week_map[year] + 1):
                WeeklyStats(position, week, year).store_data()

    for position in ["QB", "RB", "TE", "WR"]:
        for week in range(1, week_map[2021] + 1):
            Projections(position, week).store_data()

    for year in range(2016, list(week_map.keys())[0] + 1):
        YearlySnapcounts(year).store_data()
        for week in range(1, week_map[year] + 1):
            WeeklySnapcounts(week, year).store_data()

    for year in week_map.keys():
        PointsAllowed(year).store_data()

    for year in week_map.keys():
        PointsAllowed(year).store_data()


if __name__ == "__main__":
    store_all()

