"""
Implements quick and dirty tests for the data loading for fantasy
pros.
"""
import unittest
import numpy as np

from config.fantasypros import stats_type, snapcounts_type, projections_type, pa_type
from config.mapping import teams, week_map

from src.loader.fantasypros.points_allowed import PointsAllowed
from src.loader.fantasypros.projections import Projections
from src.loader.fantasypros.schedule import Schedule
from src.loader.fantasypros.snapcounts import WeeklySnapcounts, YearlySnapcounts
from src.loader.fantasypros.stats import WeeklyStats, YearlyStats


# TODO make clean with test functions

SKIP = True


class TestFantasyProsLoaderWeeklyStats(unittest.TestCase):
    @unittest.skipIf(SKIP, "extensive test")
    def test_weekly_stats_loading(self):
        for position in ["QB", "RB", "WR", "TE"]:
            for year in week_map.keys():
                for week in range(1, week_map[year] + 1):
                    df = WeeklyStats(position, week, year, refresh=True).get_data()

                    self.assertListEqual(list(stats_type[position].keys()) + ["position", "week", "year", "team"],
                                         df.columns.to_list())

                    self.assertEqual(32, len(df.team.unique()))
                    self.assertEqual(1, len(df.week.unique()))
                    self.assertEqual(1, len(df.position.unique()))

    def test_weekly_stats_QB(self):
        df = WeeklyStats("QB", 1, 2021, refresh=True).get_data()

        self.assertEqual(39, df.shape[0])
        self.assertEqual(22, df.shape[1])

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["QB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Kyler Murray', 21.0, 32.0, 65.6, 289.0, 9.0, 4.0, 1.0, 2.0, 5.0, 20.0, 1.0, 0.0, 1.0, 34.6, 34.6,
             99.3, 'QB', 1, 2021, 'ARI'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [39.0, 'Taysom Hill', 1.0, 1.0, 100.0, 3.0, 3.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 1.0, 0.2, 0.2, 53.2,
             'QB', 1, 2021, 'NO'], df.iloc[-1, :].to_list())

    def test_weekly_stats_RB(self):
        df = WeeklyStats("RB", 1, 2021, refresh=True).get_data()

        self.assertEqual(94, df.shape[0])
        self.assertEqual(22, df.shape[1])

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["RB"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Joe Mixon', 29.0, 127.0, 4.4, 19.0, 0.0, 1.0, 4.0, 4.0, 23.0, 5.8, 0.0, 0.0, 1.0, 21.0, 21.0, 98.1,
             'RB', 1, 2021, 'CIN'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [237.0, 'Rhamondre Stevenson', 1.0, 2.0, 2.0, 2.0, 0.0, 0.0, 1.0, 1.0, 9.0, 9.0, 0.0, 1.0, 1.0, -0.9, -0.9,
             50.4, 'RB', 1, 2021, 'NE'], df.iloc[-1, :].to_list())

    def test_weekly_stats_TE(self):
        df = WeeklyStats("TE", 1, 2021, refresh=True).get_data()

        self.assertEqual(66, df.shape[0])
        self.assertEqual(21, df.shape[1])

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["TE"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Rob Gronkowski', 8.0, 8.0, 90.0, 11.3, 20.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 21.0, 21.0, 97.7,
             'TE', 1, 2021, 'TB'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [222.0, 'Zach Gentry', 1.0, 1.0, -2.0, -2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.2, -0.2, 0.2, 'TE',
             1, 2021, 'PIT'], df.iloc[-1, :].to_list())

    def test_weekly_stats_WR(self):
        df = WeeklyStats("WR", 1, 2021, refresh=True).get_data()

        self.assertEqual(140, df.shape[0])
        self.assertEqual(21, df.shape[1])

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["WR"].keys()) + ["position", "week", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Tyreek Hill', 11.0, 15.0, 197.0, 17.9, 75.0, 0.0, 1.0, 1.0, 4.0, 0.0, 0.0, 1.0, 26.1, 26.1, 100.0,
             'WR', 1, 2021, 'KC'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [376.0, 'Elijah Moore', 1.0, 4.0, -3.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -0.3, -0.3, 49.1,
             'WR', 1, 2021, 'NYJ'], df.iloc[-1, :].to_list())


class TestFantasyProsLoaderYearlyStats(unittest.TestCase):
    @unittest.skipIf(SKIP, "extensive test")
    def test_yearly_stats_loading(self):
        for position in ["QB", "RB", "WR", "TE"]:
            for year in week_map.keys():
                df = YearlyStats(position, year, refresh=True).get_data()

                self.assertListEqual(list(stats_type[position].keys()) + ["position", "year", "team"],
                                     df.columns.to_list())

                self.assertEqual(1, len(df.position.unique()))

    def test_yearly_stats_QB(self):
        df = YearlyStats("QB", 2021, refresh=True).get_data()

        self.assertEqual(121, df.shape[0])
        self.assertEqual(21, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["QB"].keys()) + ["position", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Josh Allen', 409.0, 646.0, 63.3, 4407.0, 6.8, 36.0, 15.0, 26.0, 122.0, 763.0, 6.0, 3.0, 17.0, 417.7,
             24.6, 100.0, 'QB', 2021, 'team'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [121.0, 'Josh Rosen', 2.0, 11.0, 18.2, 19.0, 1.7, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, -1.2, -0.4, 0.0,
             'QB', 2021, 'team'], df.iloc[-1, :].to_list())

    def test_yearly_stats_RB(self):
        df = YearlyStats("RB", 2021, refresh=True).get_data()

        self.assertEqual(247, df.shape[0])
        self.assertEqual(21, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["RB"].keys()) + ["position", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Jonathan Taylor', 332.0, 1811.0, 5.5, 83.0, 0.0, 18.0, 40.0, 51.0, 360.0, 9.0, 2.0, 2.0, 17.0, 333.1,
             19.6, 100.0, 'RB', 2021, 'team'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [247.0, 'Trenton Cannon', 3.0, 4.0, 1.3, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 10.0, -1.6, -0.2, 0.1,
             'RB', 2021, 'team'], df.iloc[-1, :].to_list())

    def test_yearly_stats_TE(self):
        df = YearlyStats("TE", 2021, refresh=True).get_data()

        self.assertEqual(224, df.shape[0])
        self.assertEqual(20, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["TE"].keys()) + ["position", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Mark Andrews', 107.0, 153.0, 1361.0, 12.7, 43.0, 0.0, 9.0, 1.0, 0.0, 0.0, 0.0, 17.0, 194.1, 11.4,
             99.9, 'TE', 2021, 'team'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [224.0, 'Daniel Helm', 1.0, 2.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, -0.1, -0.0, 0.0, 'TE',
             2021, 'team'], df.iloc[-1, :].to_list())

    def test_yearly_stats_WR(self):
        df = YearlyStats("WR", 2021, refresh=True).get_data()

        self.assertEqual(388, df.shape[0])
        self.assertEqual(20, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))

        self.assertListEqual(list(stats_type["WR"].keys()) + ["position", "year", "team"], df.columns.to_list())

        self.assertListEqual(
            [1.0, 'Cooper Kupp', 145.0, 191.0, 1947.0, 13.4, 59.0, 0.0, 16.0, 4.0, 18.0, 0.0, 0.0, 17.0, 294.5, 17.3,
             100.0, 'WR', 2021, 'team'], df.iloc[0, :].to_list())
        self.assertListEqual(
            [388.0, 'Diontae Spencer', 1.0, 4.0, -3.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 15.0, -4.3, -0.3, 0.1,
             'WR', 2021, 'team'], df.iloc[-1, :].to_list())


class TestFantasyProsSnapcountsLoader(unittest.TestCase):
    @unittest.skipIf(SKIP, "extensive test")
    def test_weekly_snapcounts_loading(self):
        for year in week_map.keys():
            for week in range(1, week_map[year] + 1):
                df = WeeklySnapcounts(week, year, refresh=True).get_data()

                self.assertListEqual(list(snapcounts_type.keys()) + ["week", "year"], df.columns.to_list())

                self.assertEqual(1, len(df.week.unique()))
                self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())


    def test_weekly_snapcounts(self):
        df = WeeklySnapcounts(1, 2021, refresh=True).get_data()

        self.assertEqual(339, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

        self.assertListEqual(list(snapcounts_type.keys()) + ["week", "year"], df.columns.to_list())

        self.assertListEqual(
            ['Aaron Rodgers', 'QB', 'GB', 1.0, 42.0, 42.0, 74.0, 0.0, 0.0, 67.0, 67.0, 3.3, 7.9, 1, 2021],
            df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Mike Strachan', 'WR', 'IND', 1.0, 18.0, 18.0, 24.0, 0.0, 11.0, 11.0, 11.0, 2.6, 14.4, 1, 2021],
            df.iloc[-1, :].to_list())

    @unittest.skipIf(SKIP, "extensive test")
    def test_yearly_snapcounts_loading(self):
        for year in week_map.keys():
            df = YearlySnapcounts(year, refresh=True).get_data()

            self.assertListEqual(list(snapcounts_type.keys()) + ["year"], df.columns.to_list())

            self.assertEqual(1, len(df.week.unique()))
            self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

    def test_yearly_snapcounts(self):
        df = YearlySnapcounts(2021, refresh=True).get_data()

        self.assertEqual(631, df.shape[0])
        self.assertEqual(14, df.shape[1])

        self.assertEqual(["QB", "RB", "TE", "WR"], np.sort(df.position.unique()).tolist())

        self.assertListEqual(list(snapcounts_type.keys()) + ["year"], df.columns.to_list())

        self.assertListEqual(
            ['Aaron Rodgers', 'QB', 'GB', 16.0, 983.0, 61.0, 93.0, 3.0, 0.0, 57.0, 57.0, 336.3, 34.2, 2021],
            df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Michael Bandy', 'WR', 'LAC', 1.0, 10.0, 10.0, 16.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2021],
            df.iloc[-1, :].to_list())


class TestFantasyProsScheduleLoader(unittest.TestCase):
    @unittest.skipIf(SKIP, "extensive test")
    def test_schedule_loading(self):
        for year in week_map.keys():
            df = Schedule(year).get_data()

            self.assertEqual(32 * week_map[year], df.shape[0])
            self.assertEqual(5, df.shape[1])

            self.assertEqual(32, len(df.team.unique()))
            self.assertEqual(33, len(df.opponent.unique()))
            self.assertEqual(week_map[year], len(df.week.unique()))

    def test_schedule(self):
        df = Schedule(2021).get_data()

        self.assertEqual(32 * 18, df.shape[0])
        self.assertEqual(5, df.shape[1])

        self.assertListEqual(["team", "opponent", "week", "home", "year"], df.columns.to_list())

        self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(33, len(df.opponent.unique()))
        self.assertEqual(18, len(df.week.unique()))

        self.assertListEqual(["ARI", "TEN", 1, False, 2021], df.iloc[0, :].to_list())


class TestFantasyProsProjectionsLoader(unittest.TestCase):
    @unittest.skipIf(SKIP, "extensive test")
    def test_predictions_loading(self):
        for position in ["QB", "RB", "WR", "TE"]:
            for week in range(1, week_map[2021] + 1):
                df = Projections(position, week, refresh=True).get_data()

                self.assertListEqual(list(stats_type[position].keys()) + ["position", "week", "year", "team"],
                                     df.columns.to_list())

                self.assertEqual(32, len(df.team.unique()))
                self.assertEqual(1, len(df.week.unique()))
                self.assertEqual(1, len(df.position.unique()))

    def test_predictions_qb(self):
        df = Projections("QB", 1, refresh=True).get_data()

        self.assertEqual(66, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))

        self.assertListEqual(list(projections_type["QB"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertListEqual(
            ['Patrick Mahomes II', 39.1, 25.9, 314.6, 2.6, 0.5, 3.5, 18.9, 0.1, 0.1, 24.9, 'KC', 'QB', 1, 2021],
            df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Gardner Minshew II', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'PHI', 'QB', 1, 2021],
            df.iloc[-1, :].to_list())

    def test_predictions_rb(self):
        df = Projections("RB", 1, refresh=True).get_data()

        self.assertEqual(143, df.shape[0])
        self.assertEqual(13, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))

        self.assertListEqual(list(projections_type["RB"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertListEqual(
            ['Christian McCaffrey', 19.2, 80.1, 0.8, 5.4, 43.8, 0.3, 0.1, 19.0, 'CAR', 'RB', 1, 2021],
            df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Jordan Howard', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'PHI', 'RB', 1, 2021], df.iloc[-1, :].to_list())

    def test_predictions_te(self):
        df = Projections("TE", 1, refresh=True).get_data()

        self.assertEqual(112, df.shape[0])
        self.assertEqual(10, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))

        self.assertListEqual(list(projections_type["TE"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertListEqual(
            ['Travis Kelce', 6.9, 88.7, 0.8, 0.1, 13.3, 'KC', 'TE', 1, 2021], df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Deon Yelder', 0.0, 0.0, 0.0, 0.0, 0.0, 'ARI', 'TE', 1, 2021], df.iloc[-1, :].to_list())

    def test_predictions_wr(self):
        df = Projections("WR", 1, refresh=True).get_data()

        self.assertEqual(222, df.shape[0])
        self.assertEqual(13, df.shape[1])

        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(1, len(df.week.unique()))

        self.assertListEqual(list(projections_type["WR"].keys()) + ["team", "position", "week", "year"],
                             df.columns.to_list())

        self.assertListEqual(
            ['Tyreek Hill', 6.5, 93.8, 0.8, 0.8, 4.6, 0.0, 0.1, 14.6, 'KC', 'WR', 1, 2021], df.iloc[0, :].to_list())
        self.assertListEqual(
            ['Ben Skowronek', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'LAR', 'WR', 1, 2021], df.iloc[-1, :].to_list())


class TestFantasyProsPointsAllowedLoader(unittest.TestCase):
    def test_points_allowed(self):
        df = PointsAllowed(2020, refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(14, df.shape[1])

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(list(pa_type.keys()) + ["year"], df.columns.to_list())

        self.assertListEqual(
            ["ARI", 14, 19.7, 11, 19.5, 19, 22.5, 29, 6.2, 16, 7.9, 21, 4.7, 2020], df.iloc[0, :].to_list())


if __name__ == "__main__":
    unittest.main()
