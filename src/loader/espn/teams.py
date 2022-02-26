"""
Implements the yearly team stats loading from ESPN on
https://www.espn.com/nfl/stats.

Running this as a single script will fetch and store all passing,
rushing, receiving and downs statistics over a given year range for
defense and offense.
"""
from abc import ABC

from config.mapping import team_map, team_changes_map
from config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map
from src.loader.espn.espn import EspnLoader as Loader


class TeamStats(Loader, ABC):
    def __init__(self, year, season, refresh=False):
        Loader.__init__(self, year, season, refresh)
        self.to_add = {"year": self.year}


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

    def clean_data(self, df):
        """ Cleans the passing offense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["passing_yds"] = df["passing_yds"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


class RushingOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_rushing_map
        self.original_columns = ['Team', 'GP', 'ATT', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"offense_rushing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"

    def clean_data(self, df):
        """ Cleans the rushing offense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


class ReceivingOffense(OffenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = offense_receiving_map
        self.original_columns = ['Team', 'GP', 'REC', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"offense_receiving_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/offense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"

    def clean_data(self, df):
        """ Cleans the rushing offense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


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

    def clean_data(self, df):
        """ Cleans the downs offense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["penalties_yds"] = df["penalties_yds"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


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

    def clean_data(self, df):
        """ Cleans the passing defense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["passing_yds_against"] = df["passing_yds_against"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


class RushingDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_rushing_map
        self.original_columns = ['Team', 'GP', 'ATT', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"defense_rushing_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/rushing/season/{self.year}/seasontype/{self.seasontype}"

    def clean_data(self, df):
        """ Cleans the rushing defense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["rushing_yds_against"] = df["rushing_yds_against"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


class ReceivingDefense(DefenseStats, ABC):
    def __init__(self, year, season, refresh=False):
        TeamStats.__init__(self, year, season, refresh)
        self.mapping = defense_receiving_map
        self.original_columns = ['Team', 'GP', 'REC', 'YDS', 'AVG', 'YDS/G', 'LNG', 'TD', 'FUM', 'LOST']

        self.filename = f"defense_receiving_{self.year}_{self.season}.csv"
        self.dir = f"../raw/teamstats/{self.year}/"
        self.url = f"https://www.espn.com/nfl/stats/team/_/view/defense/stat/receiving/season/{self.year}/seasontype/{self.seasontype}"

    def clean_data(self, df):
        """ Cleans the receiving defense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["receiving_yds_against"] = df["receiving_yds_against"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


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

    def clean_data(self, df):
        """ Cleans the downs defense data. """
        # map columns
        df = self.map_columns(df)

        # put team abbreviation instead of full name
        df["team"] = df["team"].apply(add_team_abbreviation)

        # clean up yards in total
        df["penalties_yds"] = df["penalties_yds"].apply(transform_yards)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set types
        return df.astype(self.mapping)


def add_team_abbreviation(team):
    """ Returns team abbreviations if available. """
    if team in team_map:
        return team_map[team]
    elif team in team_changes_map:
        return team_map[team_changes_map[team]]
    else:
        print(team, "not found.")
        return team


def transform_yards(yards):
    """ Removes comma in yards stats denoting a thousand. """
    if "," in str(yards):
        return int(str(yards).replace(",", ""))
    else:
        return yards


def store_all():
    """ Stores all team stats for given year range. """
    years = (2010, 2021)
    for year in range(years[0], years[1] + 1):
        PassingDefense(year, "REG").store_data()
        RushingDefense(year, "REG").store_data()
        ReceivingDefense(year, "REG").store_data()
        DownsDefense(year, "REG").store_data()
        PassingOffense(year, "REG").store_data()
        RushingOffense(year, "REG").store_data()
        ReceivingOffense(year, "REG").store_data()
        DownsOffense(year, "REG").store_data()


if __name__ == "__main__":
    store_all()
