""" Implements quick and dirty tests for the data loading for ESPN. """
import unittest
import numpy as np

from config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map
from config.mapping import teams

from src.loader.espn.teams import PassingDefense, RushingDefense, ReceivingDefense, DownsDefense
from src.loader.espn.teams import PassingOffense, RushingOffense, ReceivingOffense, DownsOffense


# TODO make clean with test functions


class TestEspnLoader(unittest.TestCase):
    def test_defense_passing(self):
        df = PassingDefense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertListEqual(list(defense_passing_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["BUF", 17, 297, 530, 56.0, 2771, 5.7, 163.0, 73, 12, 19, 42, 276, 65.3, 2021],
                             df.iloc[0, :].to_list())

    def test_defense_rushing(self):
        df = RushingDefense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        self.assertListEqual(list(defense_rushing_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["BAL", 17, 378, 1436, 3.8, 84.5, 66, 13, 7, 1, 2021], df.iloc[0, :].to_list())

    def test_defense_receiving(self):
        df = ReceivingDefense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        self.assertListEqual(list(defense_receiving_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        # test entries
        entries_should = ["BUF", 17, 297, 3047, 10.3, 179.2, 73, 12, 9, 5, 2021]
        self.assertListEqual(entries_should, df.iloc[0, :].to_list())

    def test_offense_passing(self):
        df = PassingOffense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertListEqual(list(offense_passing_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["TB", 17, 492, 731, 67.3, 5229, 7.4, 307.6, 62, 43, 12, 23, 154, 101.6, 2021],
                             df.iloc[0, :].to_list())

    def test_offense_rushing(self):
        df = RushingOffense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        self.assertListEqual(list(offense_rushing_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["PHI", 17, 550, 2715, 4.9, 159.7, 38, 25, 17, 3, 2021], df.iloc[0, :].to_list())

    def test_offense_receiving(self):
        df = ReceivingOffense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

        self.assertListEqual(list(offense_receiving_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["TB", 17, 492, 5383, 10.9, 316.6, 62, 43, 7, 4, 2021], df.iloc[0, :].to_list())

    def test_defense_downs(self):
        df = DownsDefense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertListEqual(list(defense_downs_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["BUF", 17, 285, 108, 138, 39, 66, 214, 30.8, 16, 35, 45.7, 102, 844, 2021],
                             df.iloc[0, :].to_list())

    def test_offense_downs(self):
        df = DownsOffense(2021, "REG", refresh=True).get_data()

        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

        self.assertListEqual(list(offense_downs_map.keys()) + ["year"], df.columns.to_list())

        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

        self.assertListEqual(["KC", 17, 419, 119, 267, 33, 107, 205, 52.2, 10, 15, 66.7, 111, 925, 2021],
                             df.iloc[0, :].to_list())


if __name__ == "__main__":
    unittest.main()
