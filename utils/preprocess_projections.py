"""
Creates and stores a weekly overview of projections for a
given year. Projections are only available for season 2021.
"""
import src.preprocessing.projections.projections as projections


if __name__ == "__main__":
    for position in ["DST", "K", "QB", "RB", "TE", "WR"]:
        projections.store_accumulated_projections_weekly(2021, position)
