"""
Implements the data handling for the yearly stats from
https://www.fantasypros.com/nfl/stats/. The data is available for
every position.
"""
import os
import pandas as pd

import src.loader.loader as loader
import src.loader.stats.helpers as helpers


def fetch_stats_yearly(year, position):
    """
    Fetches the yearly stats from
    https://www.fantasypros.com/nfl/stats/.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :return: yearly stats
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_stats_yearly(year, position))


def get_stats_yearly(year, position):
    """
    Returns the yearly stats for the given year and position. Either
    loads stored file or fetches from webpage.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :return: yearly statistics with year and position added
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/yearly_stats/{year}/{position.upper()}_{year}.csv"):
        # fetch and clean the data
        df = fetch_stats_yearly(year, position)
        df = helpers.clean_stats(df, position)
        df["year"] = year
        df["position"] = position
        return df
    else:
        # load already cleaned data
        return pd.read_csv(f"../raw/yearly_stats/{year}/{position.upper()}_{year}.csv")


def get_url_stats_yearly(year, position):
    return f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"


def store_all_stats(years):
    """
    Stores all yearly stats in a given year range.

    :param years: year range to fetch schedules
    :type years: tuple
    :return: None
    """
    for position in ["QB", "WR", "RB", "TE", "DST", "K"]:
        for year in range(years[0], years[1] + 1):
            store_stats_yearly(year, position)


def store_stats_yearly(year, position):
    """
    Stores the yearly stats for a given year and position.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/yearly_stats/{year}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/yearly_stats/{year}"))
    get_stats_yearly(year, position).to_csv(f"../raw/yearly_stats/{year}/{position.upper()}_{year}.csv",
                                            index=False)


if __name__ == "__main__":
    pass

