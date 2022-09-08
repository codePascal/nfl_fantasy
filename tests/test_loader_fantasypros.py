"""
Implements quick and dirty tests for the data loading for fantasy
pros.
"""
import unittest
import numpy as np

import src.loader.fantasypros.statistics as loader

from src.config.fantasypros import stats_type, snapcounts_type, projections_type, pa_type
from src.config.mapping import teams

# TODO make clean with test functions

SKIP = True


class TestFantasyProsLoaderWeeklyStats(unittest.TestCase):
    def test_weekly_stats_QB(self):
        df = loader.WeeklyStats("QB", 1, 2021).get_data()
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["QB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

    def test_weekly_stats_RB(self):
        df = loader.WeeklyStats("RB", 1, 2021).get_data()
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["RB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

    def test_weekly_stats_TE(self):
        df = loader.WeeklyStats("TE", 1, 2021).get_data()
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["TE"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

    def test_weekly_stats_WR(self):
        df = loader.WeeklyStats("WR", 1, 2021).get_data()
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["WR"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())


class TestFantasyProsLoaderYearlyStats(unittest.TestCase):
    def test_yearly_stats_QB(self):
        df = loader.YearlyStats("QB", 2021).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["QB"].keys()) + ["position", "year", "team"], df.columns.to_list())

    def test_yearly_stats_RB(self):
        df = loader.YearlyStats("RB", 2021).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["RB"].keys()) + ["position", "year", "team"], df.columns.to_list())

    def test_yearly_stats_TE(self):
        df = loader.YearlyStats("TE", 2021).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["TE"].keys()) + ["position", "year", "team"], df.columns.to_list())

    def test_yearly_stats_WR(self):
        df = loader.YearlyStats("WR", 2021).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertListEqual(list(stats_type["WR"].keys()) + ["position", "year", "team"], df.columns.to_list())


class TestFantasyProsSnapcountsLoader(unittest.TestCase):
    def test_weekly_snapcounts(self):
        df = loader.WeeklySnapcounts(1, 2021).get_data()
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())
        self.assertListEqual(list(snapcounts_type.keys()) + ["week", "year"], df.columns.to_list())

    def test_yearly_snapcounts(self):
        df = loader.YearlySnapcounts(2021).get_data()
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())
        self.assertListEqual(list(snapcounts_type.keys()) + ["year"], df.columns.to_list())


class TestFantasyProsScheduleLoader(unittest.TestCase):
    def test_schedule(self):
        df = loader.Schedule(2021).get_data()
        self.assertListEqual(["team", "opponent", "week", "home", "year"], df.columns.to_list())
        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(33, len(df.opponent.unique()))
        self.assertEqual(18, len(df.week.unique()))


class TestFantasyProsProjectionsLoader(unittest.TestCase):
    def test_predictions_qb(self):
        df = loader.Projections("QB", 1).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertListEqual(list(projections_type["QB"].keys()) + ["position", "week", "year", "team"],
                             df.columns.to_list())

    def test_predictions_rb(self):
        df = loader.Projections("RB", 1).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertListEqual(list(projections_type["RB"].keys()) + ["position", "week", "year", "team"],
                             df.columns.to_list())

    def test_predictions_te(self):
        df = loader.Projections("TE", 1).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertListEqual(list(projections_type["TE"].keys()) + ["position", "week", "year", "team"],
                             df.columns.to_list())

    def test_predictions_wr(self):
        df = loader.Projections("WR", 1).get_data()
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertListEqual(list(projections_type["WR"].keys()) + ["position", "week", "year", "team"],
                             df.columns.to_list())


class TestFantasyProsPointsAllowedLoader(unittest.TestCase):
    def test_points_allowed(self):
        df = loader.PointsAllowed(2020).get_data()
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())
        self.assertListEqual(list(pa_type.keys()) + ["year"], df.columns.to_list())


if __name__ == "__main__":
    unittest.main()
