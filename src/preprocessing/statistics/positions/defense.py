from positions.helpers import concat_weekly_stats


def concat_weekly_defensive_stats(year, weeks):
    """
    Concatenates weekly defensive stats.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    return concat_weekly_stats(year, weeks, ["DST"])


if __name__ == "__main__":
    year = 2021
    weeks = 18
    df = concat_weekly_defensive_stats(year, weeks)



