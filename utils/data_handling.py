import pandas as pd

team_name_map = {
    "TAM": "TB",
    "KAN": "KC",
    "LAR": "LA",
    "NOR": "NO",
    "GNB": "GB",
    "NWE": "NE",
    "SFO": "SF",
    # "OAK": "LV"
}

position_map = {
    "HB": "RB",
    "FB": "RB",
    "WR/RS": "WR",
    "WR/PR": "WR",
    "FB/TE": "TE",
    "FB/RB": "RB"
}


def read_csv_file(path):
    return pd.read_csv(path)


def concat_weekly_stats(year):
    """
    Concatenates weekly stats for a given year.

    :param year: year to concatenate weekly stats
    :type year: int
    :return: weekly stats concatenated
    :rtype: pandas.DataFrame
    """
    stats = pd.DataFrame()
    for week in range(1, 18):
        weekly_stats = pd.read_csv(
            "/home/pascal/git/nfl-fantasy/data/weekly/{year}/week{week}.csv".format(year=year, week=week))
        weekly_stats["Week"] = week
        stats = pd.concat([stats, weekly_stats])
    return stats


def replace_team_names(df):
    """
    Replaces team names to given standards.

    :param df: data to replace team names
    :type df: pandas.DataFrame
    :return: data with team names replaced
    :rtype: pandas.DataFrame
    """
    return df.replace({"Tm": team_name_map})


def replace_positions(df):
    """
    Replaces positions to given standards.

    :param df: data to replace positions
    :type df: pandas.DataFrame
    :return: data with positions replaced
    :rtype: pandas.DataFrame
    """
    return df.replace({"Pos": position_map})
