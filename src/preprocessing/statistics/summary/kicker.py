"""
Concatenates kicker weekly stats with schedule.
"""
import os
import pandas as pd

import src.preprocessing.statistics.positions.kicker as kicker

import src.loader.schedule.schedule as schedule


def concat_kicker_stats(year):
    """
    Summarizes weekly stats and schedule for defense kickers into
    one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats and schedule for kickers
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(kicker.get_accumulated_stats_weekly_kicker(year),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


def get_kicker_stats_summary(year):
    """
    Returns the summarized kicker stats.

    :param year: year to summarize
    :type year: int
    :return: summarized kicker stats
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../preprocessed/summary/kicker_summary_{year}.csv"):
        return concat_kicker_stats(year)
    else:
        return pd.read_csv(f"../preprocessed/summary/kicker_summary_{year}.csv")


def store_kicker_stats_summary(year):
    """
    Stores the summarized kicker stats.

    :param year: year to summarize
    :type year: int
    :return: None
    """
    get_kicker_stats_summary(year).to_csv(f"../preprocessed/summary/kicker_summary_{year}.csv", index=False)


if __name__ == "__main__":
    pass
