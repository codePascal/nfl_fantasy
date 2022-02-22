"""
Concatenates weekly snapcount analysis for a whole season.
"""
import os
import pandas as pd

import config.mapping as mapping
import src.loader.snapcounts.weekly as snapcounts


def concat_snapcounts_weekly(year):
    """
    Concatenates weekly snapcount stats.

    :param year: year to evaluate
    :type year: int
    :return: summarized snapcount analysis for the season
    :rtype: pandas.DataFrame
    """
    # store snapcounts
    snapcount_stats = pd.DataFrame()

    # get snapcounts for each week and concat
    for week in range(1, mapping.week_map[year] + 1):
        df = snapcounts.get_snapcounts_weekly(year, week)
        snapcount_stats = pd.concat([snapcount_stats, df])

    # reset the index to start from 0
    return snapcount_stats.reset_index(drop=True)


def get_accumulated_snapcounts_weekly(year):
    """
    Returns the accumulated snapcount stats for a given year.

    :param year: year to evaluate
    :type year: int
    :return: summarized snapcount analysis for the season
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../preprocessed/snapcounts/snapcounts_summary_{year}.csv"):
        return concat_snapcounts_weekly(year)
    else:
        return pd.read_csv(f"../preprocessed/snapcounts/snapcounts_summary_{year}.csv")


def store_accumulated_snapcounts_weekly(year):
    """
    Stores the accumulated snapcount stats for a given year.

    :param year: year to evaluate
    :type year: int
    :return: None
    """
    get_accumulated_snapcounts_weekly(year).to_csv(f"../preprocessed/snapcounts/snapcounts_summary_{year}.csv",
                                                   index=False)


if __name__ == "__main__":
    pass
