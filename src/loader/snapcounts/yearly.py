"""
Implements the data handling for yearly snapcounts from
https://www.fantasypros.com/nfl/reports/snap-count-analysis/.
"""
import os
import pandas as pd

import src.loader.loader as loader
import src.loader.snapcounts.helpers as helpers


def fetch_snapcounts_yearly(year):
    """
    Fetches the yearly snapcounts from
    https://www.fantasypros.com/nfl/reports/snap-count-analysis/.

    :param year: year to fetch
    :type year: int
    :return: yearly snapcounts
    :rtype: pandas.DataFrame
    """
    return loader.get_html_content(get_url_snapcounts_yearly(year))


def get_snapcounts_yearly(year):
    """
    Returns the yearly snapcount analysis, either reads from
    stored file or fetches from webpage.

    :param year: year to fetch
    :type year: int
    :return: yearly snapcounts with year added
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../raw/yearly_snapcounts/snapcounts_{year}.csv"):
        # fetch and clean the data
        df = fetch_snapcounts_yearly(year)
        df = helpers.clean_snapcount_analysis(df)
        df["year"] = year
        return df
    else:
        # load already cleaned data
        return pd.read_csv(f"../raw/yearly_snapcounts/snapcounts_{year}.csv")


def get_url_snapcounts_yearly(year):
    return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={year}&snaps=0&range=full"


def store_all_snapcounts(years):
    """
    Stores all yearly snapcount stats in a given year range.

    :param years: year range to fetch schedules
    :type years: tuple
    :return: None
    """
    for year in range(years[0], years[1] + 1):
        store_snapcounts_yearly(year)


def store_snapcounts_yearly(year):
    """
    Stores the yearly snapcounts for a given year.

    :param year: year to fetch
    :type year: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts"))
    get_snapcounts_yearly(year).to_csv(f"../raw/yearly_snapcounts/snapcounts_{year}.csv", index=False)


if __name__ == "__main__":
    pass

