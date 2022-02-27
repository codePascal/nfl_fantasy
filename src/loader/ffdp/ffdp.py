"""
Generates .csv file from yearly stats from
https://github.com/fantasydatapros/data. The csv file contains the
players name, the year and his team for that season.

Note: it currently just assigns teams at is and without notice when
players switched teams during the season.

This script should only be run to generate the assignments and then
use these.
"""
import os
import pandas as pd

from config.mapping import teams, team_changes_map
from src.loader.fantasypros.stats import YearlyStats


class FFDPLoader:
    def __init__(self, year):
        self.year = year
        self.filename = f"players_{self.year}.csv"
        self.dir = f"../raw/players"

    def fetch_data(self):
        df = self.load_data()
        df = df.loc[:, ["Player", "Tm", "Pos"]]
        df["Tm"] = df["Tm"].apply(self.fix_team)
        df.columns = ["player", "team", "position"]
        return df

    def load_data(self):
        return pd.read_csv(f"../../data/yearly/{self.year}.csv")

    def fix_team(self, team):
        if team in teams:
            # team has not changed its name since that year year
            return team
        else:
            if team in team_changes_map["general"]:
                # abbreviation is not consistent
                return team_changes_map["general"][team]
            elif self.year in team_changes_map and team in team_changes_map[self.year]:
                # team changed its name in that year
                return team_changes_map[self.year][team]
            else:
                # back then, the team was named that
                return team

    def store_data(self):
        self.fetch_data().to_csv(os.path.join(self.dir, self.filename), index=False, header=True)

    def add_data(self):
        df = pd.DataFrame()
        for position in ["QB", "RB", "TE", "WR"]:
            yearly = YearlyStats(position, self.year).get_data()
            yearly = yearly.loc[:, ["player", "team", "position"]]
            df = pd.concat([df, yearly])
        df.to_csv(os.path.join(self.dir, self.filename), index=False, header=True)
