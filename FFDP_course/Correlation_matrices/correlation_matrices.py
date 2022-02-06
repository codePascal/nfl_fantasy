"""
Code source:
    https://www.fantasyfootballdatapros.com/course/section/9
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

pos_map = {
    "HB": "RB",
    "WR/RS": "WR",
    "WR/PS": "WR",
    "FB/TE": "TE",
    "FB/HB": "RB"
}

position_spots = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 2
}

positions = ["QB", "RB", "WR", "TE"]
columns = ["Player", "Tm", "Pos", "Week", "PPRFantasyPoints"]


def get_top_n_player_at_each_pos(data, pos, n):
    data = data.loc[data["Pos"] == pos]
    return data.groupby("Tm", as_index=False).apply(lambda x: x.nlargest(n, ["PPRFantasyPoints"]).min())


df = pd.DataFrame()
url = "https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv"
year = 2019
for week in range(1, 18):
    weekly_df = pd.read_csv(url.format(year=year, week=week))
    weekly_df["Week"] = week
    df = pd.concat([df, weekly_df])

df = df.replace({"Pos": pos_map})
df = df.loc[df["Pos"].isin(positions)]

new_df = df[columns]
new_df = new_df.groupby(["Player", "Tm", "Pos"], as_index=False).agg({"PPRFantasyPoints": np.mean})

corr_df = pd.DataFrame()
for pos, n_spots in position_spots.items():
    for n in range(1, n_spots + 1):
        pos_df = get_top_n_player_at_each_pos(new_df, pos, n)
        pos_df = pos_df.rename({"PPRFantasyPoints": f"{pos}{n}"}, axis=1)
        corr_df = pd.concat([corr_df, pos_df], axis=1)

corr_df = corr_df.dropna()
corr_df = corr_df.drop(["Pos", "Player", "Tm"], axis=1)

plt.figure(figsize=(10, 7))
sns.heatmap(corr_df.corr(), annot=True, cmap=sns.diverging_palette(0, 250))
plt.savefig("plots/heatmap_pprfantasypoints_2019.png")



