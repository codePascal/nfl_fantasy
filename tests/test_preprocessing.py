""" Implements quick and dirty tests for the preprocessing. """
import unittest

from config.fantasypros import snapcounts_type, projections_type

from preprocessing.fantasypros.projections import Projections
from preprocessing.fantasypros.snapcounts import Snapcounts
from preprocessing.fantasypros.stats import Stats
from src.preprocessing.statistics import Statistics

# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestPreprocessing(unittest.TestCase):
    def test_predictions(self):
        df = Projections("QB").get_accumulated_data()

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
        df = Snapcounts(2021).get_accumulated_data()

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
        df = Stats("QB", 2021).get_accumulated_data()

        # test content
        self.assertEqual(1, len(df.position.unique()))
        self.assertEqual(18, len(df.week.unique()))
        unique_names = df.player.unique()
        for unique_name in unique_names:
            self.assertGreater(19, len(df.loc[df["player"] == unique_name]), f"{unique_name} appears too much.")

        # test entries
        self.assertEqual("Kyler Murray", df.iloc[0, 1])
        self.assertEqual("Tim Boyle", df.iloc[-1, 1])

    @unittest.skip("Deprecated")
    def test_statistics(self):
        df = Statistics(2021).get_accumulated_data()

        # test entries
        self.assertEqual(df.iloc[0, 1], "Arizona Cardinals")
        self.assertEqual(df.iloc[-1, 1], "Jakeem Grant Sr.")


if __name__ == "__main__":
    unittest.main()
