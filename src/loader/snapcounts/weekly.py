"""
Implements the data handling for weekly snapcounts from
https://www.fantasypros.com/nfl/reports/snap-count-analysis/.
"""
import os
import pandas as pd

import config.mapping as mapping
import src.loader.loader as loader
import src.loader.snapcounts.helpers as helpers


def fetch_snapcounts_weekly(year, week):
    """
    Fetches the weekly snapcounts from
    https://www.fantasypros.com/nfl/reports/snap-count-analysis/.

    :param year: year to fetch
    :type year: int
    :param week: week to fetch
    :type week: int
    :return: weekly snapcounts
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_snapcounts_weekly(year, week))


def get_snapcounts_weekly(year, week):
    """
    Returns the weekly snapcount analysis, either reads from
    stored file or fetches from webpage.

    :param year: year to fetch
    :type year: int
    :param week: week to fetch
    :type week: int
    :return: snapcounts analysis
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/weekly_snapcounts/{year}/week_{week}.csv"):
        # fetch and clean the data
        df = fetch_snapcounts_weekly(year, week)
        df = helpers.clean_snapcount_analysis(df)
        df["week"] = week
        return df
    else:
        # load already cleaned data
        return pd.read_csv(f"../raw/weekly_snapcounts/{year}/week_{week}.csv")


def get_url_snapcounts_weekly(year, week):
    return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={week}&snaps=0&range=week&year={year}"


def store_all_snapcounts(years):
    """
    Stores all weekly snapcount stats in a given year range.

    :param years: year range to fetch schedules
    :type years: tuple
    :return: None
    """
    for year in range(years[0], years[1] + 1):
        for week in range(1, mapping.week_map[year] + 1):
            store_snapcounts_weekly(year, week)


def store_snapcounts_weekly(year, week):
    """
    Stores the weekly snapcounts for a given year and week.

    :param year: year to fetch
    :type year: int
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{year}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{year}"))
    get_snapcounts_weekly(year, week).to_csv(f"../raw/weekly_snapcounts/{year}/week_{week}.csv", index=False)


if __name__ == "__main__":
    store_all_snapcounts((2016, 2021))
