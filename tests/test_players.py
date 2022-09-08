""" Implements quick and dirty tests for the players loading. """
import unittest
import numpy as np

from src.config.mapping import week_map, teams
from src.loader.players import TeamsLoader


class TestTeamsLoader(unittest.TestCase):
    def test_teams(self):
        for year in week_map.keys():
            df = TeamsLoader(year).get_data()
            self.assertListEqual(list(np.sort(teams)), list(np.sort(df.team.unique())))

    def test_players_qb(self):
        for year in week_map.keys():
            df = TeamsLoader(year).get_data()
            for week in range(1, week_map[year] + 1):
                df_mod = df.loc[(df["week"] == week) & (df["position"] == "QB")]
                df_dropped = df_mod.drop_duplicates()
                self.assertEqual(len(df_mod), len(df_dropped), msg=f"year:{year}, week:{week}")

    def test_players_rb(self):
        for year in week_map.keys():
            df = TeamsLoader(year).get_data()
            for week in range(1, week_map[year] + 1):
                df_mod = df.loc[(df["week"] == week) & (df["position"] == "RB")]
                df_dropped = df_mod.drop_duplicates()
                self.assertEqual(len(df_mod), len(df_dropped), msg=f"year:{year}, week:{week}")

    def test_players_te(self):
        for year in week_map.keys():
            df = TeamsLoader(year).get_data()
            for week in range(1, week_map[year] + 1):
                df_mod = df.loc[(df["week"] == week) & (df["position"] == "TE")]
                df_dropped = df_mod.drop_duplicates()
                self.assertEqual(len(df_mod), len(df_dropped), msg=f"year:{year}, week:{week}")

    def test_players_wr(self):
        for year in week_map.keys():
            df = TeamsLoader(year).get_data()
            for week in range(1, week_map[year] + 1):
                df_mod = df.loc[(df["week"] == week) & (df["position"] == "WR")]
                df_dropped = df_mod.drop_duplicates()
                self.assertEqual(len(df_mod), len(df_dropped), msg=f"year:{year}, week:{week}")


if __name__ == "__main__":
    unittest.main()
