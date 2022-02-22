"""
Creates and stores a weekly overview of snapcount analysis for a
given year range. Snapcounts were recorded since 2016.
"""
import src.preprocessing.statistics.snapcounts.snapcounts as snapcounts


if __name__ == "__main__":
    to_year = 2021
    for year in range(2016, to_year + 1):
        snapcounts.store_accumulated_snapcounts_weekly(year)
