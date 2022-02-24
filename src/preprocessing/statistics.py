"""
Accumulates weekly stats with snapcounts and schedule for a season.

Running this script will store the accumulated statistics for a given
year range.
"""
import numpy as np
import pandas as pd

from abc import ABC

from config.mapping import teams, team_map, team_changes_map
from src.loader.schedule import Schedule
from src.preprocessing.preprocessing import Preprocessing
from src.preprocessing.snapcounts import Snapcounts
from src.preprocessing.stats import Stats


class Statistics(Preprocessing, ABC):
    def __init__(self, year):
        Preprocessing.__init__(self)

        self.year = year

        self.filename = f"statistics_{self.year}.csv"
        self.dir = f"../preprocessed/statistics"

    def concat_data(self):
        """ Concatenates weekly stats, snapcounts and schedule. """
        # merge stats with snapcounts
        df = pd.merge(Stats(self.year).get_accumulated_data(),
                      Snapcounts(self.year).get_accumulated_data(),
                      how="outer",
                      on=["player", "week", "year", "fantasy_points", "games", "position"])

        # clean up team names for free agents and new abbreviations
        df["team"] = df.apply(clean_up_teams, axis=1)
        df["team"] = df["team"].apply(fix_teams)
        df.drop(["team_x", "team_y"], axis=1, inplace=True)

        # the statistics are already for a single game
        df.drop(["fantasy_points_per_game", "snaps_per_game"], axis=1, inplace=True)

        # merge schedule
        df = pd.merge(df, Schedule(self.year).get_data(), how="outer", on=["team", "week", "year"])

        print(df.loc[df["team"] == "FA"])

        return df


def clean_up_teams(player):
    """ Takes players team from snapcounts if available. """
    # TODO still missing teams
    if player["team_x"] == "FA" and player["team_y"] is not np.nan:
        return player["team_y"]
    return player["team_x"]


def fix_teams(team):
    """ Updates team abbreviations to the latest ones. """
    if team not in teams and team is not np.nan:
        if team in team_changes_map.keys():
            return team_changes_map[team]
        elif team != "FA":
            print("Team abbreviation", team, "not available.")
    return team



def store_all():
    """ Accumulates and stores the accumulated statistics. """
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        Statistics(year).store_accumulated_data()


if __name__ == "__main__":
    store_all()
