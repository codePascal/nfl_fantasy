from positions.helpers import concat_weekly_stats


def concat_weekly_offensive_stats(year, weeks):
    """
    Concatenates weekly offensive stats. Takes only players into
    account that have played that week.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    return concat_weekly_stats(year, weeks, ["QB", "RB", "TE", "WR"])


if __name__ == "__main__":
    year = 2021
    weeks = 18
    df = concat_weekly_offensive_stats(year, weeks)
