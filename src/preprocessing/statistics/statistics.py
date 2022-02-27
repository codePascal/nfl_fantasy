"""
Accumulates weekly stats with snapcounts and schedule for a season.

Running this script will store the accumulated statistics for a given
year range.
"""
import numpy as np
import pandas as pd

from abc import ABC

from config.mapping import teams, team_changes_map, week_map
from src.loader.fantasypros.schedule import Schedule
from src.preprocessing.preprocessing import Preprocessing
from src.preprocessing.statistics.snapcounts import Snapcounts
from src.preprocessing.statistics.stats import Stats


class Statistics(Preprocessing, ABC):
    def __init__(self, position, year, refresh=False):
        Preprocessing.__init__(self, year, refresh)
        self.position = position
        self.year = year

        self.filename = f"statistics_{self.position}_{self.year}.csv"
        self.dir = f"../preprocessed/statistics/{self.year}"

    def concat_data(self):
        """ Concatenates weekly stats, snapcounts and schedule
        for given position. """
        # get snapcounts only for position
        snapcounts = Snapcounts(self.year, refresh=self.refresh).get_accumulated_data()
        snapcounts = snapcounts.loc[snapcounts["position"] == self.position]

        # merge with weekly accumulated stats
        stats = pd.merge(snapcounts,
                         Stats(self.position, self.year, refresh=self.refresh).get_accumulated_data(),
                         how="outer",
                         on=["player", "week", "year", "fantasy_points", "games", "position", "team"])

        # drop not relevant columns
        stats.drop(["rank", "rost", "fantasy_points_per_game", "snaps_per_game"], axis=1, inplace=True)

        # clean up teams to latest names
        stats["team"] = stats["team"].apply(fix_teams)

        # merge schedule
        stats = pd.merge(stats, Schedule(self.year).get_data(), how="outer", on=["team", "week", "year"])

        return stats


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
    for position in ["QB", "RB", "TE", "WR"]:
        for year in range(2016, 2021):
            Statistics(position, year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
