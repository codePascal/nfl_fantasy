"""
Separately summarizes statistics for defense, kicker and offense.
"""
import src.preprocessing.statistics.summary.defense as defense
import src.preprocessing.statistics.summary.kicker as kicker
import src.preprocessing.statistics.summary.offense as offense


if __name__ == "__main__":
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        defense.store_defense_stats_summary(year)
        kicker.store_kicker_stats_summary(year)
        offense.store_offense_stats_summary(year)
