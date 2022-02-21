import pandas as pd

map_type = {
    "player": str,
    "position": str,
    "team": str,
    "games": int,
    "snaps": int,
    "snaps_per_game": int,
    "snaps_percent": int,
    "rush_percent": int,
    "tgt_percent": int,
    "touch_percent": int,
    "util_percent": int,
    "fantasy_points": float,
    "points_per_100_snaps": float
}


def concat_weekly_snapcounts(year, weeks):
    """
    Concatenates weekly snapcount stats.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized snapcount analysis for the season
    :rtype: pandas.DataFrame
    """
    # store snapcounts
    snapcount_stats = pd.DataFrame()

    # get snapcounts for each week and concat
    for week in range(1, weeks + 1):
        df = get_weekly_snapcounts(year, week)
        snapcount_stats = pd.concat([snapcount_stats, df])

    # reset the index to start from 0
    return snapcount_stats.reset_index(drop=True)


def get_weekly_snapcounts(year, week):
    """
    Gets the weekly snapcounts for the given year and year.

    :param year: year to read
    :type year: int
    :param week: week to read
    :type week: int
    :return: weekly snapcounts with week
    :rtype: pandas.DataFrame
    """
    # read the data
    df = pd.read_csv(f"../raw/weekly_snapcounts/{year}/week_{week}.csv")

    # drop the unnamed column
    df.drop(df.columns[0], axis=1, inplace=True)

    # clean up and add additional data
    df = clean_snapcount_analysis(df)
    df["week"] = week

    return df


def clean_snapcount_analysis(df):
    """
    Cleans up snapcount analysis.

    :param df: analysis as read from csv
    :type df: pandas.DataFrame
    :return: cleaned snapcount analysis
    :rtype: pandas.DataFrame
    """
    # rename column names in a more descriptive manner
    df.columns = list(map_type.keys())

    # set types
    return df.astype(map_type)


if __name__ == "__main__":
    year = 2021
    weeks = 18
    df = concat_weekly_snapcounts(year, weeks)
