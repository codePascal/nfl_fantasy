""" Implements quick and dirty tests for the data loading. """
import unittest
import numpy as np

from config.fantasypros import stats_type, snapcounts_type, projections_type, pa_type
from config.mapping import teams

from loader.fantasypros.points_allowed import PointsAllowed
from loader.fantasypros.projections import Projections
from loader.fantasypros.schedule import Schedule
from loader.fantasypros.snapcounts import WeeklySnapcounts, YearlySnapcounts
from loader.fantasypros.stats import WeeklyStats, YearlyStats


# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestFantasyProsLoader(unittest.TestCase):
    def test_weekly_stats(self):
        df = WeeklyStats("QB", 1, 2021).get_data()

        # test shape
        self.assertEqual(120, df.shape[0])
        self.assertEqual(22, df.shape[1])

        # test column names
        cols_should = list(stats_type["QB"].keys()) + ["team", "position", "week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.position.unique()))

        # test entries
        entries_should = [1, "Kyler Murray", 21, 32, 65.6, 289, 9.0, 4, 1, 2, 5, 20, 1, 0, 1, 34.6, 34.6, 99.3, "ARI",
                          "QB", 1, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_yearly_stats(self):
        df = YearlyStats("QB", 2021).get_data()

        # test shape
        self.assertEqual(121, df.shape[0])
        self.assertEqual(21, df.shape[1])

        # test column names
        cols_should = list(stats_type["QB"].keys()) + ["team", "position", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.position.unique()))

        # test entries
        entries_should = [1, "Josh Allen", 409, 646, 63.3, 4407, 6.8, 36, 15, 26, 122, 763, 6, 3, 17, 417.7, 24.6,
                          100.0, "BUF", "QB", 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_weekly_snapcounts(self):
        df = WeeklySnapcounts(1, 2021).get_data()

        # test shape
        self.assertEqual(339, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(snapcounts_type.keys()) + ["week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

        # test entries
        entries_should = ["Ben Roethlisberger", "QB", "PIT", 1, 58,	58,	100, 7,	0, 62, 62, 12.0, 20.7, 1, 2021]
        self.assertListEqual(entries_should, df.iloc[1, :].to_list())

    def test_yearly_snapcounts(self):
        df = YearlySnapcounts(2021).get_data()

        # test shape
        self.assertEqual(631, df.shape[0])
        self.assertEqual(14, df.shape[1])

        # test column names
        cols_should = list(snapcounts_type.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

        # test entries
        entries_should = ["Adrian Peterson", "RB", "SEA", 4, 72, 18, 27, 53, 6, 58, 58, 22.6, 31.4, 2021]
        self.assertListEqual(entries_should, df.iloc[1, :].to_list())

    def test_schedule(self):
        df = Schedule(2021).get_data()

        # test shape
        self.assertEqual(32 * 18, df.shape[0])
        self.assertEqual(5, df.shape[1])

        # test column names
        cols_should = ["team", "opponent", "week", "home", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(33, len(df.opponent.unique()))
        self.assertEqual(18, len(df.week.unique()))

        # test entries
        entries_should = ["ARI", "TEN", 1, False, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_predictions(self):
        df = Projections("QB", 1).get_data()

        # test shape
        self.assertEqual(66, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(projections_type["QB"].keys()) + ["team", "position", "week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))

        # test entries
        entries_should = ["Patrick Mahomes II", 39.1, 25.9, 314.6, 2.6, 0.5, 3.5, 18.9, 0.1, 0.1, 24.9, "KC", "QB", 1,
                          2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_points_allowed(self):
        df = PointsAllowed(2020).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(14, df.shape[1])

        # test column names
        cols_should = list(pa_type.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["ARI", 14, 19.7, 11, 19.5, 19, 22.5, 29, 6.2, 16, 7.9, 21, 4.7, 2020]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())


if __name__ == "__main__":
    unittest.main()
