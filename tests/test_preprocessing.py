""" Implements quick and dirty tests for the preprocessing. """
import unittest

from src.preprocessing.projections import Projections
from src.preprocessing.snapcounts import Snapcounts
from src.preprocessing.stats import Stats
from src.preprocessing.statistics import Statistics

# TODO implement more specific tests
# TODO include more positions
# TODO make clean with test functions


class TestPreprocessing(unittest.TestCase):
    def test_predictions(self):
        df = Projections("QB").get_accumulated_data()

        # test entries
        self.assertEqual(df.iloc[0, 0], "Patrick Mahomes II")
        self.assertEqual(df.iloc[-1, 0], "Jacoby Brissett")

        # test weeks
        self.assertEqual(len(df.week.unique()), 18)

    def test_snapcounts(self):
        df = Snapcounts(2021).get_accumulated_data()

        # test entries
        self.assertEqual(df.iloc[0, 0], "Aaron Rodgers")
        self.assertEqual(df.iloc[-1, 0], "C.J. Saunders")

        # test weeks
        self.assertEqual(len(df.week.unique()), 18)

    def test_stats(self):
        df = Stats(2021).get_accumulated_data()

        # test entries
        self.assertEqual(df.iloc[0, 1], "Arizona Cardinals")
        self.assertEqual(df.iloc[-1, 1], "Andre Roberts")

        # test weeks and positions
        self.assertEqual(len(df.week.unique()), 18)
        self.assertEqual(len(df.position.unique()), 6)

    def test_statistics(self):
        df = Statistics(2021).get_accumulated_data()

        # test entries
        self.assertEqual(df.iloc[0, 1], "Arizona Cardinals")
        self.assertEqual(df.iloc[-1, 1], "Jakeem Grant Sr.")


if __name__ == "__main__":
    unittest.main()
