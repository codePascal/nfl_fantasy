"""
Accumulates all weekly snapcounts for a season into one.

Refreshing means, that it will, regardless if the file already
exists, accumulate the stats again. However, this does not mean that
the stats itself are refreshed.

Running this script will store all summaries for a denoted year
range or refresh them if available offline.
"""
import numpy as np
import pandas as pd
import sys

from abc import ABC

from config.mapping import week_map, team_changes_map, teams
from src.loader.fantasypros.snapcounts import WeeklySnapcounts as Loader
from src.preprocessing.preprocessing import Preprocessing


class Snapcounts(Preprocessing, ABC):
    def __init__(self, year, refresh=False):
        Preprocessing.__init__(self, year, refresh)

        # check year
        if self.year < 2016:
            sys.exit("Snapcounts are only available for seasons 2016 and onwards.")

        self.filename = f"snapcounts_summary_{self.year}.csv"
        self.dir = f"../preprocessed/snapcounts"

    def concat_data(self):
        """ Concatenates the weekly snapcounts into one. """
        df = pd.DataFrame()
        for week in range(1, week_map[self.year] + 1):
            df = pd.concat([df, Loader(week, self.year, self.refresh).get_data()])
        df = df.loc[df["games"] == 1]
        df["team"] = df["team"].apply(fix_team)
        return df.reset_index(drop=True)


def fix_team(team):
    """ Checks that latest team abbreviations are used. """
    if team not in teams and team is not np.nan:
        if team in team_changes_map.keys():
            return team_changes_map[team]
        else:
            print("Team abbreviation", team, "not available.")
    else:
        return team




def store_all():
    """ Accumulates and stores all weekly snapcounts for a season. """
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        Snapcounts(year, refresh=True).store_accumulated_data()


if __name__ == "__main__":
    store_all()
