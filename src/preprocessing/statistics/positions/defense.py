"""
Concatenates weekly defense stats for a whole season.
"""
import src.preprocessing.statistics.positions.helpers as helpers


def get_accumulated_stats_weekly_defense(year):
    """
    Returns the accumulated weekly defensive stats.

    :param year: year to evaluate
    :type year: int
    :return: summarized weekly defense stats for season
    :rtype: pandas.DataFrame
    """
    return helpers.get_accumulated_stats_weekly(year, ["DST"], f"../preprocessed/stats/defense_{year}.csv")


def store_accumulated_stats_weekly_defense(year):
    """
    Stores the accumulated weekly defensive stats.

    :param year: year to evaluate
    :type year: int
    :return: None
    """
    helpers.store_accumulated_stats_weekly(year, ["DST"], f"../preprocessed/stats/defense_{year}.csv")


if __name__ == "__main__":
    pass
