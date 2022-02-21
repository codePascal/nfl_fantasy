"""
Concatenates weekly kicker stats for a whole season.
"""
import src.preprocessing.statistics.positions.helpers as helpers


def get_accumulated_stats_weekly_kicker(year):
    """
    Returns the accumulated weekly kicker stats.

    :param year: year to evaluate
    :type year: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    return helpers.get_accumulated_stats_weekly(year, ["K"], f"../preprocessed/stats/kicker_{year}.csv")


def store_accumulated_stats_weekly_kicker(year):
    """
    Stores the accumulated weekly kicker stats.

    :param year: year to evaluate
    :type year: int
    :return: None
    """
    helpers.store_accumulated_stats_weekly(year, ["K"], f"../preprocessed/stats/kicker_{year}.csv")


if __name__ == "__main__":
    pass
