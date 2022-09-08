import unittest

import src.loader.statistics as stats


class TestLoaderStatisticsFantasyPros(unittest.TestCase):
    def test_get_weekly_stats_QB(self):
        df = stats.get_weekly_stats("QB", 1, 2021)

        self.assertEqual(40, df.shape[0])
        self.assertEqual(19, df.shape[1])

        # self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

    def test_get_weekly_stats_RB(self):
        df = stats.get_weekly_stats("RB", 1, 2021)

        self.assertEqual(107, df.shape[0])
        self.assertEqual(19, df.shape[1])

        # self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

    def test_get_weekly_stats_TE(self):
        df = stats.get_weekly_stats("TE", 1, 2021)

        self.assertEqual(69, df.shape[0])
        self.assertEqual(18, df.shape[1])

        # self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

    def test_get_weekly_stats_WR(self):
        df = stats.get_weekly_stats("WR", 1, 2021)

        self.assertEqual(150, df.shape[0])
        self.assertEqual(18, df.shape[1])

        # self.assertEqual(32, len(df.team.unique()))
        self.assertEqual(1, len(df.week.unique()))
        self.assertEqual(1, len(df.position.unique()))

    def test_get_yearly_stats(self):
        df = stats.get_yearly_stats("QB", 2021)
        self.assertEqual(84, df.shape[0])
        self.assertEqual(19, df.shape[1])

    def test_get_weekly_snapcounts(self):
        df = stats.get_weekly_snapcounts(1, 2021)
        self.assertEqual(339, df.shape[0])
        self.assertEqual(14, df.shape[1])

    def test_get_yearly_snapcounts(self):
        df = stats.get_yearly_snapcounts(2021)
        self.assertEqual(631, df.shape[0])
        self.assertEqual(14, df.shape[1])

    def test_get_projections(self):
        df = stats.get_projections("QB", 1, 2021)
        self.assertEqual(15, df.shape[1])

    def test_get_points_allowed(self):
        df = stats.get_points_allowed(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(14, df.shape[1])


class TestLoaderStatisticsEspn(unittest.TestCase):
    def test_get_offense_passing(self):
        df = stats.get_offense_passing_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

    def test_get_offense_rushing(self):
        df = stats.get_offense_rushing_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

    def test_get_offense_receiving(self):
        df = stats.get_offense_receiving_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

    def test_get_offense_downs(self):
        df = stats.get_offense_downs_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

    def test_get_defense_passing(self):
        df = stats.get_defense_passing_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])

    def test_get_defense_rushing(self):
        df = stats.get_defense_rushing_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

    def test_get_defense_receiving(self):
        df = stats.get_defense_receiving_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(11, df.shape[1])

    def test_get_defense_downs(self):
        df = stats.get_defense_downs_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(15, df.shape[1])


class TestLoaderAccumulated(unittest.TestCase):
    def test_get_accumulated_weekly_stats(self):
        df = stats.get_accumulated_weekly_stats("QB", 2021)
        self.assertEqual(678, df.shape[0])
        self.assertEqual(19, df.shape[1])

    def test_get_accumulated_yearly_stats(self):
        df = stats.get_accumulated_yearly_stats("QB")
        self.assertEqual(932, df.shape[0])
        self.assertEqual(19, df.shape[1])

    def test_get_accumulated_weekly_snapcounts(self):
        df = stats.get_accumulated_weekly_snapcounts(2021)
        self.assertEqual(5800, df.shape[0])
        self.assertEqual(14, df.shape[1])

    def test_get_accumulated_yearly_snapcounts(self):
        df = stats.get_accumulated_yearly_snapcounts()
        self.assertEqual(2880, df.shape[0])
        self.assertEqual(14, df.shape[1])

    def test_get_accumulated_projections(self):
        df = stats.get_accumulated_projections("QB")
        self.assertEqual(1059, df.shape[0])
        self.assertEqual(15, df.shape[1])

    def test_get_offense_stats(self):
        df = stats.get_offense_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(43, df.shape[1])

    def test_get_defense_stats(self):
        df = stats.get_defense_stats(2021)
        self.assertEqual(32, df.shape[0])
        self.assertEqual(43, df.shape[1])
