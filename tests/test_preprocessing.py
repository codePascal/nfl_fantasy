""" Implements quick and dirty tests for the preprocessing. """
import unittest

from config.fantasypros import snapcounts_type, projections_type

from src.preprocessing.statistics.projections import Projections
from src.preprocessing.statistics.snapcounts import Snapcounts
from src.preprocessing.statistics.stats import Stats
from src.preprocessing.statistics.statistics import Statistics
from src.preprocessing.statistics.defense import MergeDefense

# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestPreprocessing(unittest.TestCase):
    def test_predictions(self):
        df = Projections("QB", refresh=True).get_accumulated_data()

        # test column names not altered
        cols_should = list(projections_type["QB"].keys()) + ["team", "position", "week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(18, len(df.week.unique()))
        unique_names = df.player.unique()
        for unique_name in unique_names:
            self.assertGreater(19, len(df.loc[df["player"] == unique_name]))

        # test entries
        self.assertEqual("Patrick Mahomes II", df.iloc[0, 0])
        self.assertEqual("Jacoby Brissett", df.iloc[-1, 0])

    def test_snapcounts(self):
        df = Snapcounts(2021, refresh=True).get_accumulated_data()

        # test column names not altered
        cols_should = list(snapcounts_type.keys()) + ["week", "year"]
        self.assertListEqual(cols_should, df.columns.to_list())

        # test content
        self.assertEqual(18, len(df.week.unique()))
        unique_names = df.player.unique()
        for unique_name in unique_names:
            self.assertGreater(19, len(df.loc[df["player"] == unique_name]))

        # test entries
        self.assertEqual("Aaron Rodgers", df.iloc[0, 0])
        self.assertEqual("C.J. Saunders", df.iloc[-1, 0])

    def test_stats(self):
        df = Stats("QB", 2021, refresh=True).get_accumulated_data()

        # test content
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))
        unique_names = df.player.unique()
        for unique_name in unique_names:
            self.assertGreater(19, len(df.loc[df["player"] == unique_name]), f"{unique_name} appears too much.")

        # test entries
        self.assertEqual("Kyler Murray", df.iloc[0, 1])
        self.assertEqual("Tim Boyle", df.iloc[-1, 1])

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

    def test_defense(self):
        df = MergeDefense(2021, refresh=True).get_accumulated_data()

        # test content
        unique_teams = df.team.unique()
        for unique_team in unique_teams:
            self.assertEqual(1, len(df.loc[df["team"] == unique_team]), f"{unique_team} appears too much.")
        self.assertEqual(32, len(df.team.unique()))


if __name__ == "__main__":
    unittest.main()
