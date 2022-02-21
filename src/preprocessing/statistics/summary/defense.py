"""
Concatenates defense weekly stats with schedule.
"""
import os
import pandas as pd

import src.preprocessing.statistics.positions.defense as defense

import src.loader.schedule.schedule as schedule


def concat_defense_stats(year):
    """
    Summarizes weekly stats and schedule for defense into one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats and schedule for defense
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(defense.get_accumulated_stats_weekly_defense(year),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


def get_defense_stats_summary(year):
    """
    Returns the summarized defense stats.

    :param year: year to summarize
    :type year: int
    :return: summarized defense stats
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../preprocessed/summary/defense_summary_{year}.csv"):
        return concat_defense_stats(year)
    else:
        return pd.read_csv(f"../preprocessed/summary/defense_summary_{year}.csv")


def store_defense_stats_summary(year):
    """
    Stores the summarized defense stats.

    :param year: year to summarize
    :type year: int
    :return: None
    """
    get_defense_stats_summary(year).to_csv(f"../preprocessed/summary/defense_summary_{year}.csv", index=False)


if __name__ == "__main__":
    pass
