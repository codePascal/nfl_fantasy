import pandas as pd

import positions.offense as offense
import positions.defense as defense
import positions.kicker as kicker
import schedule
import snapcounts


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


def concat_offense_stats(year, weeks):
    """
    Summarizes weekly stats, snapcounts and schedule for offense into
    one.

    :param year: year to summarize
    :type year: int
    :param weeks: weeks in the season
    :type weeks: int
    :return: weekly stats, snacounts and schedule for offense
    :rtype: pandas.DataFrame
    """
    # summarize weekly stats and snapcounts
    stats = pd.merge(offense.concat_weekly_offensive_stats(year, weeks),
                     snapcounts.concat_weekly_snapcounts(year, weeks),
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


def concat_defense_stats(year, weeks):
    """
    Summarizes weekly stats and schedule for defense into one.

    :param year: year to summarize
    :type year: int
    :param weeks: weeks in the season
    :type weeks: int
    :return: weekly stats and schedule for defense
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(defense.concat_weekly_defensive_stats(year, weeks),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


def concat_kicker_stats(year, weeks):
    """
    Summarizes weekly stats and schedule for defense kickers into
    one.

    :param year: year to summarize
    :type year: int
    :param weeks: weeks in the season
    :type weeks: int
    :return: weekly stats and schedule for kickers
    :rtype: pandas.DataFrame
    """
    # merge stats with schedule
    season = pd.merge(kicker.concat_weekly_kicker_stats(year, weeks),
                      schedule.get_schedule(year),
                      how="outer",
                      on=["team", "week"])

    # drop unnecessary columns
    return season.drop(["fantasy_points_per_game"], axis=1)


if __name__ == "__main__":
    year = 2021
    weeks = 18
    concat_offense_stats(year, weeks).to_csv(f"../preprocessed/stats/offense_summary_{year}.csv", index=False)
    concat_defense_stats(year, weeks).to_csv(f"../preprocessed/stats/defense_summary_{year}.csv", index=False)
    concat_kicker_stats(year, weeks).to_csv(f"../preprocessed/stats/kicker_summary_{year}.csv", index=False)


