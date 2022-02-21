from positions.helpers import concat_weekly_stats


def concat_weekly_kicker_stats(year, weeks):
    """
    Concatenates weekly kicker stats.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    return concat_weekly_stats(year, weeks, ["K"])


if __name__ == "__main__":
    year = 2021
    weeks = 18
    df = concat_weekly_kicker_stats(year, weeks)
