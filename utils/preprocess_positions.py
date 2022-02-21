"""
Creates and stores a weekly separate overview for defense, kicker and
offense.
"""
import src.preprocessing.statistics.positions.defense as defense
import src.preprocessing.statistics.positions.kicker as kicker
import src.preprocessing.statistics.positions.offense as offense


if __name__ == "__main__":
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        defense.store_accumulated_stats_weekly_defense(year)
        kicker.store_accumulated_stats_weekly_kicker(year)
        offense.store_accumulated_stats_weekly_offense(year)
