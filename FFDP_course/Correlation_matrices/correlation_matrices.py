"""
Code source:
    https://www.fantasyfootballdatapros.com/course/section/9
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import utils.data_handling as dh

sns.set_style("whitegrid")

YEAR = 2019
SELECTOR = "PPRFantasyPoints"

position_spots = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 2,
}
positions = ["QB", "RB", "WR", "TE"]
features = ["Player", "Tm", "Pos", "Week", SELECTOR]


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


# load accumulated weekly stats
df = dh.concat_weekly_stats(YEAR)

# replace team names with standard abbreviations
df = dh.replace_team_names(df)

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

# clean up data
corr_df = corr_df.dropna()
corr_df = corr_df.drop(["Pos", "Player", "Tm"], axis=1)

# plot the correlation heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(corr_df.corr(), annot=True, cmap=sns.diverging_palette(0, 250))
plt.savefig("plots/heatmap_{selector}_{year}.png".format(selector=SELECTOR, year=YEAR))
