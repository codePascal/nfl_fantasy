"""
Evaluates the TD regression candidates for a given position regarding
the mean. A high or low touchdown total is not predictive for future
performance as these players will often regress towards the mean or
average the following year.

Play-by-play source season 2009-2018:
    https://www.kaggle.com/maxhorowitz/nflplaybyplay2009to2016?select=NFL+Play+by+Play+2009-2018+%28v5%29.csv
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

import utils.fantasy_pros as fp

sns.set_style("whitegrid")

PREPROCESSED_BASIS = True
PREPROCESSED_EST = True
PREPROCESSED_ACTUAL = False

PLAY = "rec"  # rush, pass, rec
POSITION = "RB"  # QB, RB, TE, WR


def fix_player_names(name):
    split = name.split()
    first_initial = split[0][0]
    last_name = split[1]
    return '.'.join([first_initial, last_name])


if __name__ == "__main__":
    # calculate probability of scoring a touchdown depending on
    # distance to endzone based on historical play-by-play raw
    if not PREPROCESSED_BASIS:
        # load in single chunks
        chunks = pd.read_csv("../raw/play-by-play/pbp_2009to2018.csv", iterator=True, low_memory=False,
                             chunksize=10000)

        # concat to dataframe
        df = pd.DataFrame()
        for chunk in chunks:
            df = pd.concat([df, chunk])

        # select pass or run attempts
        if PLAY == "pass" or PLAY == "rec":
            # passing/receiving: pass attempt that ended in a touchdown
            df = df.loc[:, ["pass_attempt", "pass_touchdown", "yardline_100", "two_point_attempt"]]
            df = df.rename({"pass_attempt": "attempt", "pass_touchdown": "touchdown"}, axis=1)
        elif PLAY == "rush":
            # rushing: rush attempt that ended in a touchdown
            df = df.loc[:, ["rush_attempt", "rush_touchdown", "yardline_100", "two_point_attempt"]]
            df = df.rename({"rush_attempt": "attempt", "rush_touchdown": "touchdown"}, axis=1)

        # select only normal attempts
        df = df.loc[(df["two_point_attempt"] == 0) & (df["attempt"] == 1)]

        # find probability of scoring a touchdown depending on distance to endzone
        df_prob = df.groupby("yardline_100")["touchdown"].value_counts(normalize=True)
        df_prob = pd.DataFrame({"probability_of_touchdown": df_prob.values}, index=df_prob.index).reset_index()

        # keep stats where touchdown was scored and drop column
        df_prob = df_prob.loc[(df_prob["touchdown"] == 1)]
        df_prob = df_prob.drop("touchdown", axis=1)

        # save preprocessed probability raw
        df_prob.to_csv(f"../preprocessed/td_regression/preprocessed_probability_{PLAY}.csv", index=False)
    else:
        # load preprocessed probability raw
        df_prob = pd.read_csv(f"../preprocessed/td_regression/preprocessed_probability_{PLAY}.csv")

    # plot probability of scoring a touchdown
    df_prob.plot(x="yardline_100", y="probability_of_touchdown", title=f"Probability for {PLAY}ing TD")
    plt.savefig(f"../plots/td_regression_candidates/touchdown_probability_{PLAY}.png")

    if not PREPROCESSED_EST:
        # load 2019 play-by-play raw
        chunks = pd.read_csv("../raw/play-by-play/play_by_play_2019.csv", iterator=True, low_memory=False, chunksize=10000,
                             index_col=0)
        df = pd.DataFrame()
        for chunk in chunks:
            df = pd.concat([df, chunk])

        # get player, team and distance to endzone
        df_train = pd.DataFrame()
        if PLAY == "pass":
            df_train = df.loc[:, ["passer_player_name", "posteam", "yardline_100"]]
        elif PLAY == "rec":
            df_train = df.loc[:, ["receiver_player_name", "posteam", "yardline_100"]]
        elif PLAY == "rush":
            df_train = df.loc[:, ["rusher_player_name", "posteam", "yardline_100"]]
        df_train = df_train.dropna()

        # rename features
        df_train = df_train.rename(columns={df_train.columns[0]: "player", "posteam": "team"})

        # save preprocessed training raw
        df_train.to_csv(f"../preprocessed/td_regression/preprocessed_training_{PLAY}.csv", index=False)
    else:
        # load preprocessed training raw
        df_train = pd.read_csv(f"../preprocessed/td_regression/preprocessed_training_{PLAY}.csv")

    # join probability with training
    data = df_train.merge(df_prob, how="left", on="yardline_100")

    # group by player and team and sum up expected touchdowns
    data = data.groupby(["player", "team"], as_index=False).agg({"probability_of_touchdown": np.sum}).rename(
        {"probability_of_touchdown": "Expected touchdowns"}, axis=1)
    data = data.sort_values(by="Expected touchdowns", ascending=False)

    # rank the expected touchdowns
    data["Expected touchdowns rank"] = data["Expected touchdowns"].rank(ascending=False)

    if not PREPROCESSED_ACTUAL:
        # load final stats
        chunks = pd.read_csv(f"../raw/yearly_stats/{POSITION}/{POSITION}_2019.csv", iterator=True, low_memory=False,
                             chunksize=10000)
        df = pd.DataFrame()
        for chunk in chunks:
            df = pd.concat([df, chunk])
        df = df.dropna()

        # clean stats for defined position
        df_actual = fp.clean_stats(df, POSITION)

        # get player, team and td
        if PLAY == "pass":
            df_actual = df_actual.loc[:, ["player", "team", "passing_td"]]
            df_actual = df_actual.rename({"passing_td": "touchdowns"}, axis=1)
        elif PLAY == "rec":
            df_actual = df_actual.loc[:, ["player", "team", "receiving_td"]]
            df_actual = df_actual.rename({"receiving_td": "touchdowns"}, axis=1)
        elif PLAY == "rush":
            df_actual = df_actual.loc[:, ["player", "team", "rushing_td"]]
            df_actual = df_actual.rename({"rushing_td": "touchdowns"}, axis=1)

        # clean up player names
        df_actual["player"] = df_actual["player"].apply(fix_player_names)

        # save preprocessed player raw
        df_actual.to_csv(f"../preprocessed/td_regression/preprocessed_actual_{PLAY}_{POSITION}.csv", index=False)
    else:
        df_actual = pd.read_csv(f"../preprocessed/td_regression/preprocessed_actual_{PLAY}_{POSITION}.csv")

    # merge raw and drop position
    data = df_actual.merge(data, how="left", on=["player", "team"]).dropna()

    # rename features and calculate rank of actual touchdowns
    data = data.rename({"touchdowns": "Actual touchdowns"}, axis=1)
    data["Actual touchdowns rank"] = data["Actual touchdowns"].rank(ascending=False)

    # calculate regression candidate
    data["Regression candidate"] = data["Expected touchdowns"] - data["Actual touchdowns"]
    data["Regression rank candidate"] = data["Actual touchdowns rank"] - data["Expected touchdowns rank"]

    # make simple true/false column for regression candidate
    data["Positive regression candidate"] = data["Regression candidate"] > 0

    # explore the statistics
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title(f"Positive regression candidates for {PLAY} {POSITION}")

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

    # show top five negative and positive regression candidates
    data_sorted = data.sort_values(by="Regression candidate", ascending=False).reset_index()
    for i, row in data_sorted.iterrows():
        if i <= 4 or i >= len(data_sorted) - 1 - 4:
            ax.text(
                x=row["Expected touchdowns"] + 0.1,
                y=row["Actual touchdowns"] + 0.05,
                s=row["player"]
            )

    # save
    plt.savefig(f"../plots/td_regression_candidates/regression_candidates_{PLAY}_{POSITION}.png")
