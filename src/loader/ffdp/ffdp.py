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
from config.positions import positions, offense_position_map, defense_position_map, special_position_map
from config.players import player_position_map

VERBOSE = False


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
                # use stats from github
                weekly = pd.read_csv(
                    f"https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{self.year}/week{week}.csv")
                weekly = weekly.loc[:, ["Player", "Tm", "Pos"]]
                weekly.columns = ["player", "team", "position"]
                weekly["week"] = week
                weekly["year"] = self.year
            else:
                # use snapcounts data
                weekly = pd.read_csv(f"../raw/weekly_snapcounts/{self.year}/week_{week}.csv", header=0)
                weekly = weekly.loc[:, ["player", "team", "position", "week", "year"]]

            # fix teams and positions
            weekly["team"] = weekly["team"].apply(self.fix_team)
            weekly["position"] = weekly.apply(self.fix_position, axis=1)

            # fix duplicates
            duplicates = weekly.duplicated(keep="first")
            weekly = weekly.loc[~duplicates, :]

            df = pd.concat([df, weekly])
        return df

    def fix_position(self, player):
        """ Fixes positions. """
        position = player["position"]
        if position in positions:
            return position
        elif position in offense_position_map:
            return offense_position_map[position]
        elif position in defense_position_map:
            return defense_position_map[position]
        elif position in special_position_map:
            return special_position_map[position]
        elif player["player"] in player_position_map:
            if VERBOSE:
                print(f"Mapping position {player_position_map[player['player']]} to {player['player']} in {self.year}.")
            return player_position_map[player["player"]]
        else:
            if VERBOSE:
                print(f"Failed to map position {position} for {player['player']} in {self.year}.")
            return position

    def fix_team(self, team):
        """ Fixes teams to the state of the specific year. """
        # fix uncommon abbreviations
        if team in team_changes_map:
            if VERBOSE:
                print(f"Changing {team} to {team_changes_map[team]} in {self.year}.")
            return team_changes_map[team]
        return team

    def modify_data(self):
        """ If data is already stored, modifies only teams. """
        df = self.get_data()
        df["team"] = df["team"].apply(self.fix_team)
        df["position"] = df.apply(self.fix_position, axis=1)
        return df

    def store_data(self):
        """ Stores the data. """
        if os.path.exists(os.path.join(self.dir, self.filename)):
            self.modify_data().to_csv(os.path.join(self.dir, self.filename), index=False, header=True)
        else:
            self.fetch_all().to_csv(os.path.join(self.dir, self.filename), index=False, header=True)


if __name__ == "__main__":
    for year in list(week_map.keys()):
        TeamsLoader(year).store_data()
