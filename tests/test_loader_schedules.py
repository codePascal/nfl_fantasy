import unittest

import src.loader.schedules as schedules


class TestLoaderSchedules(unittest.TestCase):
    def test_get_schedule(self):
        df = schedules.get_schedule(2021)
        self.assertEqual(32 * 18, df.shape[0])
        self.assertEqual(5, df.shape[1])
