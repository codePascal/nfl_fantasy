"""
Analyzes the correlation in fantasy points between positions for a
given year over the course of a league.

This correlation can be used to check if stacking a position might
offer better returns in points. The generated heatmap can be used
to decide if stacking a position might be useful.

Stacking a position means that one puts e.g. a WR2 and WR3 of a team
on the active rooster. If the correlation between the two position is
high, one position does not out-score the other one and vice-versa.

Code source:
    https://www.fantasyfootballdatapros.com/course/section/9
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

# YEAR year to analyse
# SELECTOR scoring scheme to analyse
YEAR = 2019
SELECTOR = "PPRFantasyPoints"

# define number of spots per position
position_spots = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 2,
}

# positions to analyse correlation
positions = ["QB", "RB", "WR", "TE"]

# features to select for overall stats
features = ["Player", "Tm", "Pos", "Week", SELECTOR]

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


def get_top_n_player_at_each_pos(data, pos, n):
    """
    Returns the n-best players on a position of a team.

    :param data: averaged fantasy points per player
    :type data: pandas.DataFrame
    :param pos: position to get n-best players
    :type pos: str
    :param n: number of the top players on position
    :type n: int
    :return: top n players per team on defined position
    :rtype: pandas.DataFrame
    """
    data = data.loc[data["Pos"] == pos]
    return data.groupby("Tm", as_index=False).apply(lambda x: x.nlargest(n, [SELECTOR]).min())


def concat_weekly_stats(year):
    """
    Concatenates weekly_stats stats for a given year.

    :param year: year to concatenate weekly stats
    :type year: int
    :return: weekly stats concatenated
    :rtype: pandas.DataFrame
    """
    stats = pd.DataFrame()
    for week in range(1, 18):
        weekly_stats = pd.read_csv(
            f"https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv")
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


if __name__ == "__main__":
    # load accumulated weekly_stats stats
    df = concat_weekly_stats(YEAR)

    # replace team names and positions with standard abbreviations
    df = replace_team_names(df)
    df = replace_positions(df)

    # limit to offensive players
    df = df.loc[df["Pos"].isin(positions)]

    # accumulate average of points for each player
    df = df[features].groupby(["Player", "Tm", "Pos"], as_index=False).agg({SELECTOR: np.mean})

    # get scored points per spot
    corr_df = pd.DataFrame()
    for pos, n_spots in position_spots.items():
        for n in range(1, n_spots + 1):
            pos_df = get_top_n_player_at_each_pos(df, pos, n)
            pos_df = pos_df.rename({SELECTOR: f"{pos}{n}"}, axis=1)
            corr_df = pd.concat([corr_df, pos_df], axis=1)

    # clean up raw
    corr_df = corr_df.dropna()
    corr_df = corr_df.drop(["Pos", "Player", "Tm"], axis=1)

    # plot the correlation heatmap
    plt.figure(figsize=(10, 7))
    sns.heatmap(corr_df.corr(), annot=True, cmap=sns.diverging_palette(0, 250))
    plt.savefig("heatmap_{selector}_{year}.png".format(selector=SELECTOR, year=YEAR))
