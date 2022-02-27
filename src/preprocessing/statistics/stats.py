"""
Accumulates weekly stats for all positions for a season into one
each.

Refreshing means, that it will, regardless if the file already
exists, accumulate the stats again. However, this does not mean that
the stats itself are refreshed.

Running this script will store all summaries for a denoted year
range or refresh them if available offline.
"""
import numpy as np
import pandas as pd

from abc import ABC

from config.mapping import week_map, teams, team_changes_map
from src.loader.fantasypros.stats import WeeklyStats as Loader
from src.preprocessing.preprocessing import Preprocessing


class Stats(Preprocessing, ABC):
    def __init__(self, position, year, refresh=False):
        Preprocessing.__init__(self, year, refresh)
        self.position = position
        self.filename = f"stats_summary_{self.position.upper()}_{self.year}.csv"
        self.dir = f"../preprocessed/stats/{self.year}"

    def concat_data(self):
        """ Concatenates the weekly stats for all positions into
        one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(self.position, week, self.year, self.refresh).get_data()])
        df = df.loc[df["games"] == 1]
        df["team"] = df["team"].apply(fix_team)
        return df.reset_index(drop=True)


def fix_team(team):
    """ Checks that latest team abbreviations are used. """
    if team not in teams and team is not np.nan:
        if team in team_changes_map.keys():
            return team_changes_map[team]
        elif team != "FA":
            print("Team abbreviation", team, "not available.")
    else:
        return team


def store_all():
    """ Accumulates and stores all weekly stats for a season. """
    years = (2010, 2021)
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        for year in range(years[0], years[1] + 1):
            Stats(position, year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
