"""
Concatenates various statistics of each player over a whole season
including stats, snapcount analysis, opponents and home/away etc.
"""
import pandas as pd

import utils.fantasy_pros as fp


def clean_up_teams(player):
    if player["team_x"] == "FA":
        return player["team_y"]
    return player["team_x"]


if __name__ == "__main__":
    # year and weeks
    year = 2021
    weeks = 18

    # get stats of each player for all weeks
    weekly_stats = fp.concat_weekly_offensive_stats(year, weeks)

    # get snapcount analysis of each player for all weeks
    snapcount_stats = fp.concat_weekly_snapcounts(year, weeks)

    # merge weekly stats with snapcount analysis
    stats = pd.merge(weekly_stats, snapcount_stats, how="outer",
                     on=["player", "week", "fantasy_points", "games", "position"])

    # clean up team names
    stats["team"] = stats.apply(clean_up_teams, axis=1)
    stats.drop(["team_x", "team_y"], axis=1, inplace=True)

    # drop unnecessary columns
    stats.drop(["fantasy_points_per_game", "snaps_per_game"], axis=1, inplace=True)

    # get schedule
    schedule = pd.read_csv(f"../data/schedules/schedule_{year}.csv")
    schedule = fp.clean_schedule(schedule)

    # merge stats with schedule
    season = pd.merge(stats, schedule, how="outer", on=["week", "team"])

    # store offense summary
    season.to_csv(f"../preprocessed/stats/offense_summary_{year}.csv", index=False)
