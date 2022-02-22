"""
Implements the data handling of weekly stats from
https://www.fantasypros.com/nfl/stats/. Data is available for each
week and position.
"""
import os
import pandas as pd

import config.mapping as mapping
import src.loader.loader as loader
import src.loader.stats.helpers as helpers


def fetch_stats_weekly(year, position, week):
    """
    Fetches weekly stats from
    https://www.fantasypros.com/nfl/stats/.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: weekly stats
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_stats_weekly(year, position, week))


def get_stats_weekly(year, position, week):
    """
    Returns the weekly stats for the given year, week and position,
    either reads stored file or fetches from webpage.

    :param year: year to read
    :type year: int
    :param position: position to read
    :type position: str
    :param week: week to read
    :type week: int
    :return: weekly statistics with week and position added
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/weekly_stats/{year}/{position.upper()}/week_{week}.csv"):
        # fetch and clean the data
        df = fetch_stats_weekly(year, position, week)
        df = helpers.clean_stats(df, position)
        df["week"] = week
        df["position"] = position
        return df
    else:
        # load already cleaned data
        return pd.read_csv(f"../raw/weekly_stats/{year}/{position.upper()}/week_{week}.csv")


def get_url_stats_weekly(year, position, week):
    return f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&week={week}&range=week"


def store_all_stats(years):
    """
    Stores all weekly stats in a given year range.

    :param years: year range to fetch schedules
    :type years: tuple
    :return: None
    """
    for position in ["QB", "WR", "RB", "TE", "DST", "K"]:
        for year in range(years[0], years[1] + 1):
            for week in range(1, mapping.week_map[year] + 1):
                store_stats_weekly(year, position, week)


def store_stats_weekly(year, position, week):
    """
    Stores the weekly stats for a given year, position and week.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/weekly_stats/{year}/{position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/weekly_stats/{year}/{position.upper()}"))
    get_stats_weekly(year, position, week).to_csv(f"../raw/weekly_stats/{year}/{position.upper()}/week_{week}.csv",
                                                  index=False)


if __name__ == "__main__":
    store_all_stats((2016, 2021))
