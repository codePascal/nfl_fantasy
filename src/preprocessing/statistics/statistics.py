"""
Concatenates statistics including schedule and snapcounts
(if available).
"""
import pandas as pd

import src.preprocessing.statistics.positions.defense as defense
import src.preprocessing.statistics.positions.kicker as kicker
import src.preprocessing.statistics.positions.offense as offense
import src.preprocessing.statistics.snapcounts.snapcounts as snapcounts

import src.loader.schedule.schedule as schedule


def clean_up_teams(player):
    """
    Assigns team names from snapcounts (if available) if not
    available from weekly stats.
    :param player: players data
    :type player: pandas.Series
    :return: updated team name if available
    :rtype: str
    """
    if player["team_x"] == "FA":
        return player["team_y"]
    return player["team_x"]


def concat_defense_stats(year):
    """
    Summarizes weekly stats and schedule for defense into one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats and schedule for defense
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(defense.get_accumulated_tats_weekly_defense(year),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


def concat_kicker_stats(year):
    """
    Summarizes weekly stats and schedule for defense kickers into
    one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats and schedule for kickers
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(kicker.get_accumulated_stats_weekly_kicker(year),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


def concat_offense_stats(year):
    """
    Summarizes weekly stats, snapcounts and schedule for offense into
    one.

    :param year: year to summarize
    :type year: int
    :return: weekly stats, snacounts and schedule for offense
    :rtype: pandas.DataFrame
    """
    # summarize weekly stats and snapcounts
    stats = pd.merge(offense.get_accumulated_stats_weekly_offense(year),
                     snapcounts.get_accumulated_snapcounts_weekly(year),
                     how="outer",
                     on=["player", "week", "fantasy_points", "games", "position"])

    # clean up team names
    stats["team"] = stats.apply(clean_up_teams, axis=1)
    stats.drop(["team_x", "team_y"], axis=1, inplace=True)

    # drop unnecessary columns
    stats.drop(["fantasy_points_per_game", "snaps_per_game"], axis=1, inplace=True)

    # merge stats with schedule
    season = pd.merge(stats, schedule.get_schedule(year), how="outer", on=["week", "team"])

    return season


if __name__ == "__main__":
    year = 2021
    concat_offense_stats(year).to_csv(f"../preprocessed/stats/offense_summary_{year}.csv", index=False)
    concat_defense_stats(year).to_csv(f"../preprocessed/stats/defense_summary_{year}.csv", index=False)
    concat_kicker_stats(year).to_csv(f"../preprocessed/stats/kicker_summary_{year}.csv", index=False)


