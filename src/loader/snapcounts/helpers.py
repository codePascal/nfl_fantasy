# maps the column name and type to more descriptive manner
map_type = {
    "player": str,
    "position": str,
    "team": str,
    "games": int,
    "snaps": int,
    "snaps_per_game": int,
    "snaps_percent": int,
    "rush_percent": int,
    "tgt_percent": int,
    "touch_percent": int,
    "util_percent": int,
    "fantasy_points": float,
    "points_per_100_snaps": float
}


def clean_snapcount_analysis(df):
    """
    Cleans up snapcount analysis.

    :param df: analysis as read from csv
    :type df: pandas.DataFrame
    :return: cleaned snapcount analysis
    :rtype: pandas.DataFrame
    """
    # drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # rename column names in a more descriptive manner
    df.columns = list(map_type.keys())

    # transform snaps
    df["snaps"] = df["snaps"].apply(transform_snaps)

    # set types
    return df.astype(map_type)


def transform_snaps(snaps):
    """
    Removes comma in snap stats denoting thousand.

    :param yards: accomplished snaps
    :type yards: str
    :return: accomplished snaps in new format
    :rtype: int
    """
    if "," in str(snaps):
        return int(str(snaps).replace(",", ""))
    else:
        return snaps
