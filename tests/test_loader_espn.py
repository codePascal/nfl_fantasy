""" Implements quick and dirty tests for the data loading for ESPN. """
import unittest
import numpy as np

import src.loader.espn.statistics as loader

from src.config.espn import defense_passing_map, defense_rushing_map, defense_receiving_map, defense_downs_map
from src.config.espn import offense_passing_map, offense_rushing_map, offense_receiving_map, offense_downs_map
from src.config.mapping import teams


# TODO make clean with test functions


class TestEspnLoader(unittest.TestCase):
    def test_defense_passing(self):
        df = loader.PassingDefense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(defense_passing_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_defense_rushing(self):
        df = loader.RushingDefense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])
        self.assertListEqual(list(defense_rushing_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_defense_receiving(self):
        df = loader.ReceivingDefense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])
        self.assertListEqual(list(defense_receiving_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_offense_passing(self):
        df = loader.PassingOffense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(offense_passing_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_offense_rushing(self):
        df = loader.RushingOffense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])
        self.assertListEqual(list(offense_rushing_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_offense_receiving(self):
        df = loader.ReceivingOffense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])
        self.assertListEqual(list(offense_receiving_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_defense_downs(self):
        df = loader.DownsDefense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(defense_downs_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())

    def test_offense_downs(self):
        df = loader.DownsOffense(2021, "REG").get_data()
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])
        self.assertListEqual(list(offense_downs_map.keys()) + ["year"], df.columns.to_list())
        self.assertEqual(np.sort(teams).tolist(), np.sort(df.iloc[:, 0].to_list()).tolist())


if __name__ == "__main__":
    unittest.main()
