"""
Implements data handling for data fetched from
https://www.espn.com/nfl/stats. If the data is not available offline,
it is freshly fetched from the website.
"""
import itertools
import pandas as pd

from abc import ABC

from config.mapping import teams, team_map, team_changes_map, week_map
from config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map

from src.loader.loader import Loader


class EspnLoader(Loader, ABC):
    def __init__(self, year, season):
        Loader.__init__(self)
        self.year = year
        self.season = season
        self.seasontype = self.get_season_type(self.season)
        self.skip = 0

    def get_html_content(self):
        tables = self.get_table(self.get_soup(self.get_request()))
        idx = list(itertools.chain.from_iterable(self.get_table_data(tables[0])))
        content = self.get_table_data(tables[1])
        return self.transform_to_frame([idx, content])

    @staticmethod
    def get_table(soup):
        return soup.find(class_="ResponsiveTable").find_all("table")

    @staticmethod
    def get_season_type(season):
        if season == "PRE":
            return 1
        elif season == "REG":
            return 2
        elif season == "POST":
            return 3

    def transform_to_frame(self, data):
        idx = data[0]
        content = data[1]
        if self.skip > 0:
            idx = idx[self.skip:]
            content = content[self.skip:]
        df = pd.DataFrame(content[1:], index=idx[1:], columns=content[0])
        df.index = df.index.set_names([idx[0]])
        df.reset_index(inplace=True)
        return df


class TeamStats(EspnLoader, ABC):
    def __init__(self, year, season):
        EspnLoader.__init__(self, year, season)
        self.to_add = {"year": self.year}

    def add_columns(self, df):
        df["team"] = df["team"].apply(self.add_team_abbreviation)
        return df

    @staticmethod
    def add_team_abbreviation(team):
        if team in teams:
            return team
        elif team in team_map:
            return team_map[team]
        elif team in team_changes_map:
            return team_map[team_changes_map[team]]
        else:
            print(team, "not found.")
            return team


class OffenseStats(TeamStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)


class PassingOffense(OffenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"offense_passing_{self.year}_{self.season}.csv"
        self.mapping = offense_passing_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/passing/season/{self.year}/seasontype/{self.seasontype}"


class RushingOffense(OffenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"offense_rushing_{self.year}_{self.season}.csv"
        self.mapping = offense_rushing_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"


class ReceivingOffense(OffenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"offense_receiving_{self.year}_{self.season}.csv"
        self.mapping = offense_receiving_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"


class DownsOffense(OffenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"offense_downs_{self.year}_{self.season}.csv"
        self.mapping = offense_downs_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/downs/season/{self.year}/seasontype/{self.seasontype}"

        # ugly but yes, table has two headers...
        self.skip = 1


class DefenseStats(TeamStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)


class PassingDefense(DefenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"defense_passing_{self.year}_{self.season}.csv"
        self.mapping = defense_passing_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/passing/season/{self.year}/seasontype/{self.seasontype}"


class RushingDefense(DefenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"defense_rushing_{self.year}_{self.season}.csv"
        self.mapping = defense_rushing_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"


class ReceivingDefense(DefenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"defense_receiving_{self.year}_{self.season}.csv"
        self.mapping = defense_receiving_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"


class DownsDefense(DefenseStats, ABC):
    def __init__(self, year, season):
        TeamStats.__init__(self, year, season)
        self.dir = f"../raw/teamstats/{self.year}/"
        self.filename = f"defense_downs_{self.year}_{self.season}.csv"
        self.mapping = defense_downs_map
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/downs/season/{self.year}/seasontype/{self.seasontype}"

        # ugly but yes, table has two headers...
        self.skip = 1


def store_all():
    for year in week_map.keys():
        PassingOffense(year, "REG").store_data()
        RushingOffense(year, "REG").store_data()
        ReceivingOffense(year, "REG").store_data()
        DownsOffense(year, "REG").store_data()
        PassingDefense(year, "REG").store_data()
        RushingDefense(year, "REG").store_data()
        ReceivingDefense(year, "REG").store_data()
        DownsDefense(year, "REG").store_data()


if __name__ == "__main__":
    store_all()
