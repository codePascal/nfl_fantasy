"""
Generates .csv file from weekly stats from
https://github.com/fantasydatapros/data. The csv file contains the
players name, the year and his team for that week and season.

As the season 2021 is not covered there, the snapcounts are taken
to generate such .csv file.

This script should only be run to generate the assignments and then
use these.
"""
import os
import pandas as pd

from config.mapping import team_changes_map, week_map
from src.loader.fantasypros.snapcounts import WeeklySnapcounts


class TeamsLoader:
    def __init__(self, year):
        self.year = year
        self.filename = f"players_{self.year}.csv"
        self.dir = f"../raw/players"

    def get_data(self):
        """ Returns data. """
        return pd.read_csv(os.path.join(self.dir, self.filename))

    def fetch_all(self):
        """ Reads the stats and transforms into player, position,
        team, week and year only. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            if self.year < 2021:
                # use stats from fantasypros data github
                weekly = pd.read_csv(f"../../data/weekly/{self.year}/week{week}.csv")
                weekly = weekly.loc[:, ["Player", "Tm", "Pos"]]
                weekly["Tm"] = weekly["Tm"].apply(self.fix_team)
                weekly.columns = ["player", "team", "position"]
                weekly["week"] = week
                weekly["year"] = self.year
            else:
                # use snapcounts data
                weekly = WeeklySnapcounts(week, self.year, refresh=True).get_data()
                weekly = weekly.loc[:, ["player", "team", "position", "week", "year"]]
                weekly["team"] = weekly["team"].apply(self.fix_team)
            df = pd.concat([df, weekly])
        return df

    def fix_team(self, team):
        """ Fixes teams to the state of the specific year. """
        # fix uncommon abbreviations
        if team in team_changes_map["general"]:
            # print("Updating", team)
            team = team_changes_map["general"][team]

        # iterate through the years
        if self.year < 2016 and team == "LAR":
            return "STL"
        elif self.year >= 2016 and team == "STL":
            return "LAR"
        elif self.year < 2017 and team == "LAC":
            return "SD"
        elif self.year >= 2017 and team == "SD":
            return "LAC"
        elif self.year < 2020 and team == "LV":
            return "OAK"
        elif self.year >= 2020 and team == "OAK":
            return "LV"
        else:
            return team

    def modify_data(self):
        """ If data is already stored, modifies only teams. """
        df = self.get_data()
        df["team"] = df["team"].apply(self.fix_team)
        df["test"] = "test"
        return df

    def store_data(self):
        """ Stores the data. """
        if os.path.exists(os.path.join(self.dir, self.filename)):
            self.modify_data().to_csv(os.path.join(self.dir, self.filename), index=False, header=True)
        self.fetch_all().to_csv(os.path.join(self.dir, self.filename), index=False, header=True)


if __name__ == "__main__":
    for year in list(week_map.keys()):
        TeamsLoader(year).store_data()
