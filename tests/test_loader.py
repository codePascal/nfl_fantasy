""" Implements quick and dirty tests for the data loading. """
import unittest
import numpy as np

from config.fantasypros import stats_type, snapcounts_type, projections_type, pa_type
from config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map
from config.mapping import teams

from src.loader.fantasypros.points_allowed import PointsAllowed
from src.loader.fantasypros.projections import Projections
from src.loader.fantasypros.schedule import Schedule
from src.loader.fantasypros.snapcounts import WeeklySnapcounts, YearlySnapcounts
from src.loader.fantasypros.stats import WeeklyStats, YearlyStats

from src.loader.espn.teams import PassingDefense, RushingDefense, ReceivingDefense, DownsDefense
from src.loader.espn.teams import PassingOffense, RushingOffense, ReceivingOffense, DownsOffense


# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestFantasyProsLoader(unittest.TestCase):
    def test_weekly_stats(self):
        df = WeeklyStats("QB", 1, 2021, refresh=True).get_data()

        # test shape
        self.assertEqual(120, df.shape[0])
        self.assertEqual(22, df.shape[1])

        # test column names
        cols_should = list(stats_type["QB"].keys()) + ["team", "position", "week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(32, len(df.team.unique()))

        # test entries
        entries_should = [1, "Kyler Murray", 21, 32, 65.6, 289, 9.0, 4, 1, 2, 5, 20, 1, 0, 1, 34.6, 34.6, 99.3, "ARI",
                          "QB", 1, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_yearly_stats(self):
        df = YearlyStats("QB", 2021, refresh=True).get_data()

        # test shape
        self.assertEqual(121, df.shape[0])
        self.assertEqual(21, df.shape[1])

        # test column names
        cols_should = list(stats_type["QB"].keys()) + ["team", "position", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(32, len(df.team.unique()))

        # test entries
        entries_should = [1, "Josh Allen", 409, 646, 63.3, 4407, 6.8, 36, 15, 26, 122, 763, 6, 3, 17, 417.7, 24.6,
                          100.0, "BUF", "QB", 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_weekly_snapcounts(self):
        df = WeeklySnapcounts(1, 2021, refresh=True).get_data()

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
        df = YearlySnapcounts(2021, refresh=True).get_data()

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
        df = Projections("QB", 1, refresh=True).get_data()

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
        df = PointsAllowed(2020, refresh=True).get_data()

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


class TestEspnLoader(unittest.TestCase):
    def test_defense_passing(self):
        df = PassingDefense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(defense_passing_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["BUF", 17, 297, 530, 56.0, 2771, 5.7, 163.0, 73, 12, 19, 42, 276, 65.3, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_defense_rushing(self):
        df = RushingDefense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        # test column names
        cols_should = list(defense_rushing_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["BAL", 17, 378, 1436, 3.8, 84.5, 66, 13, 7, 1, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_defense_receiving(self):
        df = ReceivingDefense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        # test column names
        cols_should = list(defense_receiving_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["BUF", 17, 297, 3047, 10.3, 179.2, 73, 12, 9, 5, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_offense_passing(self):
        df = PassingOffense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(offense_passing_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["TB", 17, 492, 731, 67.3, 5229, 7.4, 307.6, 62, 43, 12, 23, 154, 101.6, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_offense_rushing(self):
        df = RushingOffense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        # test column names
        cols_should = list(offense_rushing_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["PHI", 17, 550, 2715, 4.9, 159.7, 38, 25, 17, 3, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_offense_receiving(self):
        df = ReceivingOffense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        # test column names
        cols_should = list(offense_receiving_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["TB", 17, 492, 5383, 10.9, 316.6, 62, 43, 7, 4, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_defense_downs(self):
        df = DownsDefense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(defense_downs_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["BUF", 17, 285, 108, 138, 39, 66, 214, 30.8, 16, 35, 45.7, 102, 844, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_offense_downs(self):
        df = DownsOffense(2021, "REG", refresh=True).get_data()

        # test shape
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        # test column names
        cols_should = list(offense_downs_map.keys()) + ["year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["KC", 17, 419, 119, 267, 33, 107, 205, 52.2, 10, 15, 66.7, 111, 925, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())


if __name__ == "__main__":
    unittest.main()