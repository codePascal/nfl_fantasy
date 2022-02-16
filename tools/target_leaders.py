"""
Analyzes target leaders overall. Targets represent the number of
times a pass is thrown to a player, regardless whether a catch was
made. Highly targeted players offer greater upside, since each target
is an opportunity to accumulate a reception, receiving yards or a
touchdown
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


if __name__ == "__main__":
    # year
    year = 2021

    # load summary of offense
    df = pd.read_csv(f"../preprocessed/stats/offense_summary_{year}.csv")

    # extract player, week and receiving targets
    df = df.loc[:, ["player", "week", "team", "games", "receiving_tgt", "position"]]

    # take only RB, WR, TE
    df = df.loc[(df["position"].isin(["RB", "TE", "WR"]))]

    # add weekly targets as column
    weeks = df.week.unique()
    for week in weeks:
        df[f"week_{week}"] = df.loc[df["week"] == week].loc[:, "receiving_tgt"]

    # drop week and targets as they are now contained in single columns
    df.drop(["week", "receiving_tgt"], axis=1, inplace=True)

    # group to reduce size
    if len(weeks) == 17:
        df = df.groupby(["player", "team", "position"], as_index=False).agg({
            "games": np.sum,
            "week_1": np.sum,
            "week_2": np.sum,
            "week_3": np.sum,
            "week_4": np.sum,
            "week_5": np.sum,
            "week_6": np.sum,
            "week_7": np.sum,
            "week_8": np.sum,
            "week_9": np.sum,
            "week_10": np.sum,
            "week_11": np.sum,
            "week_12": np.sum,
            "week_13": np.sum,
            "week_14": np.sum,
            "week_15": np.sum,
            "week_16": np.sum,
            "week_17": np.sum,
        })
    elif len(weeks) == 18:
        df = df.groupby(["player", "team", "position"], as_index=False).agg({
            "games": np.sum,
            "week_1": np.sum,
            "week_2": np.sum,
            "week_3": np.sum,
            "week_4": np.sum,
            "week_5": np.sum,
            "week_6": np.sum,
            "week_7": np.sum,
            "week_8": np.sum,
            "week_9": np.sum,
            "week_10": np.sum,
            "week_11": np.sum,
            "week_12": np.sum,
            "week_13": np.sum,
            "week_14": np.sum,
            "week_15": np.sum,
            "week_16": np.sum,
            "week_17": np.sum,
            "week_18": np.sum,
        })

    # calculate total targets and average per game
    df["total_receiving_tgt"] = df.iloc[:, 4:].sum(axis=1)
    df["receiving_tgt_per_game"] = df.loc[:, "total_receiving_tgt"] / df.loc[:, "games"]

    # add rank for total targets and average targets
    df = df.sort_values(by="total_receiving_tgt", ascending=False)
    df["total_receiving_tgt_rank"] = df["total_receiving_tgt"].rank(ascending=False)
    df = df.sort_values(by="receiving_tgt_per_game", ascending=False)
    df["receiving_tgt_per_game_rank"] = df["receiving_tgt_per_game"].rank(ascending=False)

    # store
    df.to_csv(f"../reports/target_leaders/target_leaders_{year}.csv", index=False)

    # limit to top 30 of position
    for position in ["WR", "RB", "TE"]:
        df_pos = df.loc[(df["position"] == position)]
        df_pos = df_pos.sort_values(by="total_receiving_tgt", ascending=False)
        df_pos["rank"] = df_pos["total_receiving_tgt"].rank(ascending=False)
        df_pos = df_pos.loc[df_pos["rank"] < 50]

        # select only weeks to plot
        df_pos.set_index("player", drop=True, inplace=True)
        df_pos = df_pos.loc[:, [f"week_{i}" for i in weeks]]

        # plot horizontal barplot
        ax = df_pos.plot.barh(stacked=True, legend=False, figsize=(10, 30))
        plt.title(f"Receiving targets per game - Top {position}")
        plt.xlabel("total receiving targets")
        plt.tight_layout()
        plt.savefig(f"../plots/target_leaders/target_leaders_{position}_{year}.png")
