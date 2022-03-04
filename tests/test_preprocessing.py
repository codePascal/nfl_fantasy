""" Implements quick and dirty tests for the preprocessing. """
import unittest
import numpy as np

from config.fantasypros import snapcounts_type, projections_type, stats_type

from src.preprocessing.statistics.projections import Projections
from src.preprocessing.statistics.snapcounts import Snapcounts
from src.preprocessing.statistics.stats import Stats
from src.preprocessing.statistics.statistics import Statistics
from src.preprocessing.statistics.teststats import Defense, Offense


# TODO make clean with test functions


class TestPreprocessingStats(unittest.TestCase):
    def test_stats_qb(self):
        df = Stats("QB", 2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(22, df.shape[1])
        self.assertListEqual(list(stats_type["QB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertEqual(
            [1.0, 'Kyler Murray', 21.0, 32.0, 65.6, 289.0, 9.0, 4.0, 1.0, 2.0, 5.0, 20.0, 1.0, 0.0, 1.0, 34.6, 34.6,
             99.3, 'QB', 1, 2021, 'ARI'], df.iloc[0, :].to_list())
        self.assertEqual(
            [120.0, 'Tim Boyle', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 1.0, -0.1, -0.1, 0.2,
             'QB', 18, 2021, 'DET'], df.iloc[-1, :].to_list())

    def test_stats_rb(self):
        df = Stats("RB", 2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(22, df.shape[1])
        self.assertListEqual(list(stats_type["RB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertEqual(
            [1.0, 'Joe Mixon', 29.0, 127.0, 4.4, 19.0, 0.0, 1.0, 4.0, 4.0, 23.0, 5.8, 0.0, 0.0, 1.0, 21.0, 21.0, 98.1,
             'RB', 1, 2021, 'CIN'], df.iloc[0, :].to_list())
        self.assertEqual(
            [240.0, 'Mike Davis', 6.0, 30.0, 5.0, 9.0, 0.0, 0.0, 3.0, 3.0, -2.0, -0.7, 0.0, 2.0, 1.0, -1.2, -1.2, 49.7,
             'RB', 18, 2021, 'ATL'], df.iloc[-1, :].to_list())

    def test_stats_te(self):
        df = Stats("TE", 2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(21, df.shape[1])
        self.assertListEqual(list(stats_type["TE"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertEqual(
            [1.0, 'Rob Gronkowski', 8.0, 8.0, 90.0, 11.3, 20.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 21.0, 21.0, 97.7,
             'TE', 1, 2021, 'TB'], df.iloc[0, :].to_list())
        self.assertEqual(
            [214.0, 'Blake Bell', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.2, 'TE', 18,
             2021, 'KC'], df.iloc[-1, :].to_list())

    def test_stats_wr(self):
        df = Stats("WR", 2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(21, df.shape[1])
        self.assertListEqual(list(stats_type["WR"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertEqual(
            [1.0, 'Tyreek Hill', 11.0, 15.0, 197.0, 17.9, 75.0, 0.0, 1.0, 1.0, 4.0, 0.0, 0.0, 1.0, 26.1, 26.1, 100.0,
             'WR', 1, 2021, 'KC'], df.iloc[0, :].to_list())
        self.assertEqual(
            [368.0, 'Andre Roberts', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, -2.0, -2.0, 0.1, 'WR',
             18, 2021, 'LAC'], df.iloc[-1, :].to_list())


class TestPreprocessingSnapcounts(unittest.TestCase):
    def test_snapcounts(self):
        df = Snapcounts(2021, refresh=True).get_accumulated_data()

        self.assertEqual(18, len(df.week.unique()))
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(snapcounts_type.keys()) + ["week", "year"], df.columns.to_list())

        self.assertEqual(['Aaron Rodgers', 'QB', 'GB', 1.0, 42.0, 42.0, 74.0, 0.0, 0.0, 67.0, 67.0, 3.3, 7.9, 1, 2021],
                         df.iloc[0, :].to_list())
        self.assertEqual(['C.J. Saunders', 'WR', 'CAR', 1.0, 15.0, 15.0, 20.0, 0.0, 13.0, 13.0, 13.0, 1.1, 7.3, 18,
                          2021], df.iloc[-1, :].to_list())


class TestPreprocessingProjections(unittest.TestCase):
    def test_predictions_qb(self):
        df = Projections("QB", refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(projections_type["QB"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertEqual(
            ['Patrick Mahomes II', 39.1, 25.9, 314.6, 2.6, 0.5, 3.5, 18.9, 0.1, 0.1, 24.9, 'KC', 'QB', 1, 2021],
            df.iloc[0, :].to_list())
        self.assertEqual(['Jacoby Brissett', 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 'MIA', 'QB', 18, 2021],
                         df.iloc[-1, :].to_list())

    def test_predictions_rb(self):
        df = Projections("RB", refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(13, df.shape[1])
        self.assertListEqual(list(projections_type["RB"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertEqual(
            ['Christian McCaffrey', 19.2, 80.1, 0.8, 5.4, 43.8, 0.3, 0.1, 19.0, 'CAR', 'RB', 1, 2021],
            df.iloc[0, :].to_list())
        self.assertEqual(
            ['Reggie Gilliam', 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'BUF', 'RB', 18, 2021], df.iloc[-1, :].to_list())

    def test_predictions_te(self):
        df = Projections("TE", refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(10, df.shape[1])
        self.assertListEqual(list(projections_type["TE"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertEqual(['Travis Kelce', 6.9, 88.7, 0.8, 0.1, 13.3, 'KC', 'TE', 1, 2021], df.iloc[0, :].to_list())
        self.assertEqual(['Ross Dwelley', 0.0, 0.0, 0.0, 0.0, 0.0, 'SF', 'TE', 18, 2021], df.iloc[-1, :].to_list())

    def test_predictions_wr(self):
        df = Projections("WR", refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertEqual(13, df.shape[1])
        self.assertListEqual(list(projections_type["WR"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertEqual(
            ['Tyreek Hill', 6.5, 93.8, 0.8, 0.8, 4.6, 0.0, 0.1, 14.6, 'KC', 'WR', 1, 2021], df.iloc[0, :].to_list())
        self.assertEqual(
            ['Marcus Kemp', 0.1, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 'KC', 'WR', 18, 2021], df.iloc[-1, :].to_list())


class TestPreprocessingTeamStats(unittest.TestCase):
    def test_defense(self):
        df = Defense(2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        unique_teams = df.team.unique()
        for unique_team in unique_teams:
            self.assertEqual(1, len(df.loc[df["team"] == unique_team]), f"{unique_team} appears too much.")

    def test_offense(self):
        df = Offense(2021, refresh=True).get_accumulated_data()

        self.assertEqual(32, len(df.team.unique()))
        unique_teams = df.team.unique()
        for unique_team in unique_teams:
            self.assertEqual(1, len(df.loc[df["team"] == unique_team]), f"{unique_team} appears too much.")


class TestPreprocessingStatistics(unittest.TestCase):
    def test_statistics(self):
        df = Statistics("QB", 2016, refresh=True).get_accumulated_data()

        # test content
        unique_names = df.player.unique()
        for unique_name in unique_names:
            self.assertGreater(19, len(df.loc[df["player"] == unique_name]), f"{unique_name} appears too much.")
        # TODO fix me
        # self.assertEqual(33, len(df.team.unique()))
        # TODO fix me
        # self.assertEqual(33, len(df.opponent.unique()))


if __name__ == "__main__":
    unittest.main()
