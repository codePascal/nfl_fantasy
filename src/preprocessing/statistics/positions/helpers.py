import os
import pandas as pd

import config.config as config
import src.loader.stats.weekly as stats


def concat_stats_weekly(year, positions):
    """
    Concatenates weekly stats for given positions. Takes only players
    into account that have played that week.

    :param year: year to evaluate
    :type year: int
    :param positions: positions to include
    :type positions: list of str
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    # store statistics
    weekly_stats = pd.DataFrame()

    # get statistics for each week and concat
    for position in positions:
        for week in range(1, config.week_map[year] + 1):
            df = stats.get_stats_weekly(year, position, week)
            df.drop("rank", axis=1, inplace=True)
            weekly_stats = pd.concat([weekly_stats, df])

    # reset the index to start from 0
    return weekly_stats.reset_index(drop=True)


def get_accumulated_stats_weekly(year, positions, path):
    """
    Returns the accumulated weekly stats for a given year and
    positions.

    :param year: year to evaluate
    :type year: int
    :param positions: positions to include
    :type positions: list of str
    :param path: path where file is stored if available
    :type path: str
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(path):
        return concat_stats_weekly(year, positions)
    else:
        return pd.read_csv(path)


def store_accumulated_stats_weekly(year, positions, path):
    """
    Stores the accumulated weekly stats for a given year and
    positions.

    :param year: year to evaluate
    :type year: int
    :param positions: positions to include
    :type positions: list of str
    :param path: path where file is stored if available
    :type path: str
    :return: None
    """
    get_accumulated_stats_weekly(year, positions, path).to_csv(path, index=False)


if __name__ == "__main__":
    pass

