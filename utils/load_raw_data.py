"""
Loads projections, schedule, snapcounts and stats data for given year
range.
"""
import src.loader.projections.projections as projections
import src.loader.schedule.schedule as schedule
import src.loader.snapcounts.weekly as snap_weekly
import src.loader.snapcounts.yearly as snap_yearly
import src.loader.stats.weekly as stats_weekly
import src.loader.stats.yearly as stats_yearly


if __name__ == "__main__":
    years = (2016, 2021)
    projections.store_all_projections()
    schedule.store_all_schedules(years)
    snap_weekly.store_all_snapcounts(years)
    snap_yearly.store_all_snapcounts(years)
    stats_weekly.store_all_stats(years)
    stats_yearly.store_all_stats(years)
