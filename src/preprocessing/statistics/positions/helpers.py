import pandas as pd


# maps the column name and type to more descriptive manner
map_type = {
    "DST": {
        "rank": int,
        "player": str,
        "defense_sacks": int,
        "defense_ints": int,
        "fumble_recovery": int,
        "fumble_forced": int,
        "defense_td": int,
        "defense_safety": int,
        "defense_spc_td": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "K": {
        "rank": int,
        "player": str,
        "field_goal": int,
        "field_goal_att": int,
        "pct": float,
        "lg": int,
        "1-19": int,
        "20-29": int,
        "30-39": int,
        "40-49": int,
        "50+": int,
        "XPT": int,
        "XPA": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "QB": {
        "rank": int,
        "player": str,
        "passing_cmp": int,
        "passing_att": int,
        "passing_pct": float,
        "passing_yds": int,
        "passing_ya": float,
        "passing_td": int,
        "passing_int": int,
        "passing_sacks": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "RB": {
        "rank": int,
        "player": str,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_ya": float,
        "rushing_lg": int,
        "rushing_20p": int,
        "rushing_td": int,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "TE": {
        "rank": int,
        "player": str,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_lg": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    },
    "WR": {
        "rank": int,
        "player": str,
        "receiving_rec": int,
        "receiving_tgt": int,
        "receiving_yds": int,
        "receiving_yr": float,
        "receiving_lg": int,
        "receiving_20p": int,
        "receiving_td": int,
        "rushing_att": int,
        "rushing_yds": int,
        "rushing_td": int,
        "fumbles_lost": int,
        "games": int,
        "fantasy_points": float,
        "fantasy_points_per_game": float,
        "rost": float
    }
}


def concat_weekly_stats(year, weeks, positions):
    """
    Concatenates weekly offensive stats. Takes only players into
    account that have played that week.

    :param year: year to evaluate
    :type year: int
    :param weeks: number of weeks of the season
    :type weeks: int
    :return: summarized weekly stats for season
    :rtype: pandas.DataFrame
    """
    # store statistics
    weekly_stats = pd.DataFrame()

    # get statistics for each week and concat
    for position in positions:
        for week in range(1, weeks + 1):
            df = get_weekly_stats(year, week, position)
            df.drop("rank", axis=1, inplace=True)
            weekly_stats = pd.concat([weekly_stats, df])

    # reset the index to start from 0
    return weekly_stats.reset_index(drop=True)


def get_weekly_stats(year, week, position):
    """
    Gets the weekly stats for the given year, week and position.

    :param year: year to read
    :type year: int
    :param week: week to read
    :type week: int
    :param position: position to read
    :type position: str
    :return: weekly statistics with week and position added
    :rtype: pandas.DataFrame
    """
    # read the data
    df = pd.read_csv(f"../raw/weekly_stats/{year}/{position}/week_{week}.csv")

    # drop the unnamed column
    df.drop(df.columns[0], axis=1, inplace=True)

    # clean up and add additional data
    df = clean_stats(df, position)
    df["week"] = week
    df["position"] = position

    return df


def clean_stats(df, position):
    """
    Clean the stats found here:
    https://www.fantasypros.com/nfl/stats/

    :param df: data loaded from csv
    :type df: pandas.DataFrame
    :param position: position to clean
    :type position: str
    :return: cleaned data
    :rtype: pandas.DataFrame
    """
    # assign better column names
    df.columns = list(map_type[position].keys())

    # clean up general columns
    df["team"] = df.apply(get_team, axis=1)
    df["player"] = df["player"].apply(transform_name)
    df["rost"] = df["rost"].apply(transform_rost)

    # clean up specific columns
    if position == "DST":
        pass
    elif position == "K":
        pass
    elif position == "QB":
        df["passing_yds"] = df["passing_yds"].apply(transform_yards)
        df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    elif position == "RB":
        df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
        df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
    elif position == "TE":
        df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
        df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)
    elif position == "WR":
        df["receiving_yds"] = df["receiving_yds"].apply(transform_yards)
        df["rushing_yds"] = df["rushing_yds"].apply(transform_yards)

    # map the types of the columns
    return df.astype(map_type[position])


def get_team(player):
    """
    Extracts team from player entry.

    :param player: Player stats
    :type player: pandas.Series
    :return: players team
    :rtype: str
    """
    return player["player"].split('(')[1].split(')')[0]


def transform_name(name):
    """
    Removes team from players name.

    :param name: player name and team
    :type name: str
    :return: player name only
    :rtype: str
    """
    return name.split('(')[0]


def transform_yards(yards):
    """
    Removes comma in yards stats denoting thousand.

    :param yards: accomplished yards
    :type yards: str
    :return: accomplished yards in new format
    :rtype: int
    """
    if "," in str(yards):
        return int(str(yards).replace(",", ""))
    else:
        return yards


def transform_rost(rost):
    """
    Removes the rost percentage sign.

    :param rost: percentage of roosts in all leagues including %
    :type rost: str
    :return: percentage of roosts in all league excluding %
    :rtype: str
    """
    return rost[:-1]
