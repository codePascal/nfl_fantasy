"""
Concatenates weekly projections for a whole season.
"""
import os
import pandas as pd

import config.mapping as mapping
import src.loader.projections.projections as projections


def concat_projections_weekly(year, position):
    """
    Concatenates weekly projections for position.

    :param year: year to evaluate
    :type year: int
    :param position: position to evaluate
    :type position: str
    :return: summarized projections for the season and position
    :rtype: pandas.DataFrame
    """
    # store snapcounts
    proj = pd.DataFrame()

    # get snapcounts for each week and concat
    for week in range(1, mapping.week_map[year] + 1):
        df = projections.get_projections(position, week)
        proj = pd.concat([proj, df])

    # reset the index to start from 0
    return proj.reset_index(drop=True)


def get_accumulated_projections_weekly(year, position):
    """
    Returns the accumulated projections for a given year and position.

    :param year: year to evaluate
    :type year: int
    :param position: position to evaluate
    :type position: str
    :return: summarized projections for the season and position
    :rtype: pandas.DataFrame
    """
    if not os.path.exists(f"../preprocessed/projections/projections_summary_{year}_{position}.csv"):
        return concat_projections_weekly(year, position)
    else:
        return pd.read_csv(f"../preprocessed/projections/projections_summary_{year}_{position}.csv")


def store_accumulated_projections_weekly(year, position):
    """
    Stores the accumulated projections for a given year and position.

    :param year: year to evaluate
    :type year: int
    :param position: position to evaluate
    :type position: str
    :return: None
    """
    get_accumulated_projections_weekly(year, position).to_csv(
        f"../preprocessed/projections/projections_summary_{year}_{position}.csv", index=False)


if __name__ == "__main__":
    pass
