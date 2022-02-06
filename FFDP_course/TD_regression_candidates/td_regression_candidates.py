"""
Evaluates TD regression RB candidates for season 2020.

Code source:
    https://www.fantasyfootballdatapros.com/course/section/8
Play-by-play source season 2009-2018:
    https://www.kaggle.com/maxhorowitz/nflplaybyplay2009to2016?select=NFL+Play+by+Play+2009-2018+%28v5%29.csv
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")

PREPROCESSED_BASIS = False
PREPROCESSED_EST = False
PREPROCESSED_ACTUAL = False

PLAYERS = []


def fix_yardline(row):
    yardline = row["YardLineFixed"]
    direction = row["YardLineDirection"]
    if direction == "OPP":
        return yardline
    else:
        return 100 - yardline


def fix_player_names(name):
    split = name.split()
    first_initial = split[0][0].upper()
    last_name = split[1].upper()
    return '.'.join([first_initial, last_name])


if not PREPROCESSED_BASIS:
    # load in single chunks
    chunks = pd.read_csv("data/nfl_playbyplay_2009to2018_v5.csv", iterator=True, low_memory=False, chunksize=10000)

    # concat
    df = pd.DataFrame()
    for chunk in chunks:
        df = pd.concat([df, chunk])

    # slice into wanted features
    rushing_df = df[["rush_attempt", "rush_touchdown", "yardline_100", "two_point_attempt"]]
    rushing_df = rushing_df.loc[(rushing_df["two_point_attempt"] == 0) & (rushing_df["rush_attempt"] == 1)]

    # find probability of scoring a touchdown depending on distance to endzone
    rushing_df_prob = rushing_df.groupby("yardline_100")["rush_touchdown"].value_counts(normalize=True)
    rushing_df_prob = pd.DataFrame({"probability_of_touchdown": rushing_df_prob.values},
                                   index=rushing_df_prob.index).reset_index()

    # keep stats where touchdown was scored and drop column
    rushing_df_prob = rushing_df_prob.loc[rushing_df_prob["rush_touchdown"] == 1]
    rushing_df_prob = rushing_df_prob.drop("rush_touchdown", axis=1)

    # save preprocessed probability data
    rushing_df_prob.to_csv("data/preprocessed_probability_rushing.csv", index=False)

else:
    rushing_df_prob = pd.read_csv("data/preprocessed_probability_rushing.csv")

# plot probability of scoring a touchdown
rushing_df_prob.plot(x="yardline_100", y="probability_of_touchdown", title="Probability for rushing TD")
plt.savefig("plots/touchdown_probability_rushing.png")

if not PREPROCESSED_EST:
    # load 2019 play-by-play data
    url = "https://raw.githubusercontent.com/fantasydatapros/data/74b84c5fb2371b954b52b4f67ae5220930d57861/2019pbp.csv"
    chunks = pd.read_csv(url, iterator=True, low_memory=False, chunksize=10000, index_col=0)
    df = pd.DataFrame()
    for chunk in chunks:
        df = pd.concat([df, chunk])

    # get necessary data and drop non-rushing plays
    rushing_df_estimate = df[["RushingPlayer", "OffenseTeam", "YardLineFixed", "YardLineDirection"]]
    rushing_df_estimate = rushing_df_estimate.dropna()

    # modify yardline records
    rushing_df_estimate["yardline_100"] = rushing_df_estimate.apply(fix_yardline, axis=1)

    # rename features
    rushing_df_estimate = rushing_df_estimate.rename({
        "RushingPlayer": "Player",
        "OffenseTeam": "Tm"
    }, axis=1).drop(["YardLineFixed", "YardLineDirection"], axis=1)

    # save preprocessed training data
    rushing_df_estimate.to_csv("data/preprocessed_estimates_rushing.csv", index=False)

else:
    rushing_df_estimate = pd.read_csv("data/preprocessed_estimates_rushing.csv")

# join probability with actual data
data = rushing_df_estimate.merge(rushing_df_prob, how="left", on="yardline_100")

# group by player and team and sum up expected touchdowns
data = data.groupby(["Player", "Tm"], as_index=False).agg({"probability_of_touchdown": np.sum}).rename(
    {"probability_of_touchdown": "Expected touchdowns"}, axis=1)
data = data.sort_values(by="Expected touchdowns", ascending=False)

# rank the expected touchdowns
data["Expected touchdowns rank"] = data["Expected touchdowns"].rank(ascending=False)

if not PREPROCESSED_ACTUAL:
    # load final stats
    url = 'https://raw.githubusercontent.com/fantasydatapros/data/master/yearly/2019.csv'
    chunks = pd.read_csv(url, iterator=True, low_memory=False, chunksize=10000)
    df = pd.DataFrame()
    for chunk in chunks:
        df = pd.concat([df, chunk])

    # slice into wanted features
    actual = df[["Player", "Tm", "Pos", "RushingTD"]]

    # clean up team names
    actual = actual.replace({"Tm": team_name_map})

    # clean up player names
    actual["Player"] = actual["Player"].apply(fix_player_names)

    # keep only RBs
    actual = actual.loc[actual["Pos"] == "RB"]

    # save preprocessed player data
    actual.to_csv("data/preprocessed_player_rushing.csv", index=False)
else:
    actual = pd.read_csv("data/preprocessed_player_rushing.csv")

# merge data and drop position
data = actual.merge(data, how="left", on=["Player", "Tm"]).dropna()
data = data.drop("Pos", axis=1)

# rename features and calculate rank of actual touchdowns
data = data.rename({"RushingTD": "Actual touchdowns"}, axis=1)
data["Actual touchdowns rank"] = data["Actual touchdowns"].rank(ascending=False)

# calculate regression candidate
data["Regression candidate"] = data["Expected touchdowns"] - data["Actual touchdowns"]
data["Regression rank candidate"] = data["Actual touchdowns rank"] - data["Expected touchdowns rank"]

# make simple true/false column for regression candidate
data["Positive regression candidate"] = data["Regression candidate"] > 0

# explore the statistics
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title("Positive regression candidates for rushing (RB)")

# plot expected vs actual touchdowns and incorporate regression candidate values
sns.scatterplot(
    x="Expected touchdowns",
    y="Actual touchdowns",
    hue="Positive regression candidate",
    data=data,
    palette=['r', 'g']
)

# plot line denoting border to positive/negative regression candidate
max_actual_td = int(data["Actual touchdowns"].max())
max_expected_td = int(data["Expected touchdowns"].max())
max_td = max(max_actual_td, max_expected_td)
sns.lineplot(x=range(max_td), y=range(max_td))

# show notable players
for _, row in data.iterrows():
    if row["Player"] in PLAYERS:
        ax.text(
            x=row["Expected touchdowns"] + 0.1,
            y=row["Actual touchdowns"] + 0.05,
            s=row["Player"]
        )

# save
plt.savefig("plots/regression_candidates_rushing")
