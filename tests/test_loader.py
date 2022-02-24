""" Implements quick and dirty tests for the data loading. """
import unittest

from config.mapping import stats_type, snapcounts_type, projections_type, pa_type

from src.loader.points_allowed import PointsAllowed
from src.loader.projections import Projections
from src.loader.schedule import Schedule
from src.loader.snapcounts import WeeklySnapcounts, YearlySnapcounts
from src.loader.stats import WeeklyStats, YearlyStats

# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestLoader(unittest.TestCase):
    def test_weekly_stats(self):
        df = WeeklyStats("QB", 1, 2021).get_data()

        # test column names
        fixed_cols = list(stats_type["QB"].keys()) + ["team", "position", "week", "year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[0, 1], "Kyler Murray")
        self.assertEqual(df.iloc[0, 5], 289)
        self.assertEqual(df.iloc[0, 17], 99.3)
        self.assertEqual(df.iloc[0, 18], "ARI")
        self.assertEqual(df.iloc[0, 19], "QB")
        self.assertEqual(df.iloc[0, 20], 1)
        self.assertEqual(df.iloc[0, 21], 2021)

    def test_yearly_stats(self):
        df = YearlyStats("QB", 2021).get_data()

        # test column names
        fixed_cols = list(stats_type["QB"].keys()) + ["team", "position", "year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[0, 1], "Josh Allen")
        self.assertEqual(df.iloc[0, 5], 4407)
        self.assertEqual(df.iloc[0, 17], 100.0)
        self.assertEqual(df.iloc[0, 18], "BUF")
        self.assertEqual(df.iloc[0, 19], "QB")
        self.assertEqual(df.iloc[0, 20], 2021)

    def test_weekly_snapcounts(self):
        df = WeeklySnapcounts(1, 2021).get_data()

        # test column names
        fixed_cols = list(snapcounts_type.keys()) + ["week", "year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[1, 0], "Ben Roethlisberger")
        self.assertEqual(df.iloc[1, 4], 58)
        self.assertEqual(df.iloc[1, 13], 1)
        self.assertEqual(df.iloc[1, 14], 2021)

    def test_yearly_snapcounts(self):
        df = YearlySnapcounts(2021).get_data()

        # test column names
        fixed_cols = list(snapcounts_type.keys()) + ["year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[1, 0], "Adrian Peterson")
        self.assertEqual(df.iloc[1, 4], 72)
        self.assertEqual(df.iloc[1, 13], 2021)

    def test_schedule(self):
        df = Schedule(2021).get_data()

        # test column names
        fixed_cols = ["team", "opponent", "week", "home", "year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[0, 0], "ARI")
        self.assertEqual(df.iloc[0, 1], "TEN")
        self.assertEqual(df.iloc[0, 2], 1)
        self.assertEqual(df.iloc[0, 3], False)
        self.assertEqual(df.iloc[0, 4], 2021)

    def test_predictions(self):
        df = Projections("QB", 1).get_data()

        # test column names
        fixed_cols = list(projections_type["QB"].keys()) + ["team", "position", "week", "year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[0, 0], "Patrick Mahomes II")
        self.assertEqual(df.iloc[0, 11], "KC")
        self.assertEqual(df.iloc[0, 12], "QB")
        self.assertEqual(df.iloc[0, 13], 1)
        self.assertEqual(df.iloc[0, 14], 2021)

    def test_points_allowed(self):
        df = PointsAllowed(2020).get_data()

        # test column names
        fixed_cols = list(pa_type.keys()) + ["year"]
        df_cols = df.columns
        for i in range(len(fixed_cols)):
            self.assertEqual(df_cols[i], fixed_cols[i])

        # test entries
        self.assertEqual(df.iloc[0, 0], "ARI")
        self.assertEqual(df.iloc[0, 3], 11)
        self.assertEqual(df.iloc[0, 6], 22.5)
        self.assertEqual(df.iloc[0, 13], 2020)


if __name__ == "__main__":
    unittest.main()

