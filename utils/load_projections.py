""" Loads projections available. """
from config.mapping import week_map
from src.loader.projections import Projections


if __name__ == "__main__":
    # load projections
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        for week in range(1, week_map[2021] + 1):
            Projections(position, week).store_data()

