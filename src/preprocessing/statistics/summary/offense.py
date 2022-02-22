"""
Concatenates offense weekly stats with snapcounts and schedule.
"""
import os
import pandas as pd

import src.preprocessing.statistics.positions.offense as offense
import src.preprocessing.statistics.snapcounts.snapcounts as snapcounts

import src.loader.schedule.schedule as schedule


def clean_up_teams(player):
    """
    Assigns team names from snapcounts (if available) if not
    available from weekly stats.
    :param player: players data
    :type player: pandas.Series
    :return: updated team name if available
    :rtype: str
    """
    if player["team_x"] == "FA":
        return player["team_y"]
    return player["team_x"]


def concat_offense_stats(year):
    """
    Summarizes weekly stats, snapcounts and schedule for offense into
    one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats, snacounts and schedule for offense
    :rtype: pandas.DataFrame
    """
    # summarize weekly stats and snapcounts
    stats = pd.merge(offense.get_accumulated_stats_weekly_offense(year),
                     snapcounts.get_accumulated_snapcounts_weekly(year),
                     how="outer",
                     on=["player", "week", "fantasy_points", "games", "position"])

    # clean up team names
    stats["team"] = stats.apply(clean_up_teams, axis=1)
    stats.drop(["team_x", "team_y"], axis=1, inplace=True)

    # drop unnecessary columns
    stats.drop(["fantasy_points_per_game", "snaps_per_game"], axis=1, inplace=True)

    # merge stats with schedule
    season = pd.merge(stats, schedule.get_schedule(year), how="outer", on=["week", "team"])

    # add year
    season["year"] = year

    return season


def get_offense_stats_summary(year):
    """
    Returns the summarized offense stats.

    :param year: year to summarize
    :type year: int
    :return: summarized offense stats
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../preprocessed/summary/offense_summary_{year}.csv"):
        return concat_offense_stats(year)
    else:
        return pd.read_csv(f"../preprocessed/summary/offense_summary_{year}.csv")


def store_offense_stats_summary(year):
    """
    Stores the summarized offense stats.

    :param year: year to summarize
    :type year: int
    :return: None
    """
    get_offense_stats_summary(year).to_csv(f"../preprocessed/summary/offense_summary_{year}.csv", index=False)


if __name__ == "__main__":
    pass
