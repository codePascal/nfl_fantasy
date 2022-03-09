"""
Implements data handling for data fetched from
https://www.espn.com/nfl/stats. If the data is not available offline,
it is freshly fetched from the website.
"""
import bs4
import itertools
import pandas as pd
import requests

from abc import ABC

from config.mapping import teams, team_map, team_changes_map, week_map
from config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map

from src.loader.loader import Loader


class EspnLoader(Loader, ABC):
    def __init__(self, year, season, refresh=False):
        Loader.__init__(self, refresh)
        self.year = year
        self.season = season
        self.seasontype = self.get_season_type(self.season)
        self.skip = 0

    def get_html_content(self):
        """ Reads HTML content and returns data table. """
        # get HTML config
        print("Fetching from", self.url)
        req = requests.get(self.url)

        # observe HTML output -> https://webformatter.com/html
        # print(req.text)

        # get table raw
        soup = bs4.BeautifulSoup(req.content, "html.parser")
        tables = soup.find(class_="ResponsiveTable").find_all("table")
        idx = list(itertools.chain.from_iterable(self.get_table_data(tables[0])))
        content = self.get_table_data(tables[1])

        # in case table has two headers:
        if self.skip > 0:
            idx = idx[self.skip:]
            content = content[self.skip:]

        # parse to table
        data = pd.DataFrame(content[1:], index=idx[1:], columns=content[0])
        data.index = data.index.set_names([idx[0]])
        data.reset_index(inplace=True)

        return data

    @staticmethod
    def get_season_type(season):
        if season == "PRE":
            return 1
        elif season == "REG":
            return 2
        elif season == "POST":
            return 3


class TeamStats(EspnLoader, ABC):
    def __init__(self, year, season, refresh=False):
        EspnLoader.__init__(self, year, season, refresh)
        self.to_add = {"year": self.year}

    def clean_data(self, df):
        """ Cleans the team data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(self.add_team_abbreviation)

        # fix a thousand notations
        for column in df.columns.to_list():
            df[column] = df[column].apply(self.fix_thousands)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)

    @staticmethod
    def add_team_abbreviation(team):
        """ Returns team abbreviations if available. """
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
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)


class PassingOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_passing_map
        self.original_columns = ['Team', 'GP', 'CMP', 'ATT', 'CMP%', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'INT', 'SACK',
                                 'SYL', 'RTG']

        self.filename = f"offense_passing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/passing/season/{self.year}/seasontype/{self.seasontype}"


class RushingOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_rushing_map
        self.original_columns = ['Team', 'GP', 'ATT', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"offense_rushing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"


class ReceivingOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_receiving_map
        self.original_columns = ['Team', 'GP', 'REC', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"offense_receiving_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"


class DownsOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_downs_map
        self.original_columns = ['Team', 'GP', 'TOTAL', 'RUSH', 'PASS', 'PEN', 'MADE', 'ATT', 'PCT', 'MADE', 'ATT',
                                 'PCT', 'TOTAL', 'YDS']

        self.filename = f"offense_downs_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/downs/season/{self.year}/seasontype/{self.seasontype}"

        # ugly but yes, table has two headers...
        self.skip = 1


class DefenseStats(TeamStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)


class PassingDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_passing_map
        self.original_columns = ['Team', 'GP', 'CMP', 'ATT', 'CMP%', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'INT', 'SACK',
                                 'SYL', 'RTG']

        self.filename = f"defense_passing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/passing/season/{self.year}/seasontype/{self.seasontype}"


class RushingDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_rushing_map
        self.original_columns = ['Team', 'GP', 'ATT', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"defense_rushing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"


class ReceivingDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_receiving_map
        self.original_columns = ['Team', 'GP', 'REC', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"defense_receiving_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"


class DownsDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_downs_map
        self.original_columns = ['Team', 'GP', 'TOTAL', 'RUSH', 'PASS', 'PEN', 'MADE', 'ATT', 'PCT', 'MADE', 'ATT',
                                 'PCT', 'TOTAL', 'YDS']

        self.filename = f"defense_downs_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/downs/season/{self.year}/seasontype/{self.seasontype}"

        # ugly but yes, table has two headers...
        self.skip = 1



if __name__ == "__main__":
    pass
