"""
Concatenates weekly offense stats for a whole season.
"""
import src.preprocessing.statistics.positions.helpers as helpers


def get_accumulated_stats_weekly_offense(year):
    """
    Returns accumulated weekly offensive stats. Takes only players
    into account that have played that week.

    :param year: year to evaluate
    :type year: int
    :return: summarized weekly offense stats for season
    :rtype: pandas.DataFrame
    """
    return helpers.get_accumulated_stats_weekly(year, ["QB", "RB", "TE", "WR"],
                                                f"../preprocessed/stats/offense_{year}.csv")


def store_accumulated_stats_weekly_offense(year):
    """
    Stores the accumulated weekly offensive stats.

    :param year: year to evaluate
    :type year: int
    :return: None
    """
    helpers.store_accumulated_stats_weekly(year, ["QB", "RB", "TE", "WR"], f"../preprocessed/stats/offense_{year}.csv")


if __name__ == "__main__":
    pass
