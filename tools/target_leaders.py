"""
Analyzes target leaders overall. Targets represent the number of
times a pass is thrown to a player, regardless whether a catch was
made. Highly targeted players offer greater upside, since each target
is an opportunity to accumulate a reception, receiving yards or a
touchdown.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

from src.preprocessing.statistics.statistics import Statistics


if __name__ == "__main__":
    # year
    year = 2021

    # position
    position = "WR"  # RB, TE, WR

    # load position data
    df = Statistics(position, year).get_accumulated_data()

    # extract data
    df = df.loc[:, ["player", "week", "team", "games", "receiving_tgt"]]

    # add weekly targets as column
    weeks = df.week.unique()
    for week in weeks:
        df[f"week_{week}"] = df.loc[df["week"] == week].loc[:, "receiving_tgt"]

    # drop week and targets as they are now contained in single columns
    df.drop(["week", "receiving_tgt"], axis=1, inplace=True)

    # group to reduce size
    if len(weeks) == 17:
        df = df.groupby(["player", "team"], as_index=False).agg({
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
        df = df.groupby(["player", "team"], as_index=False).agg({
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
    df.to_csv(f"../reports/target_leaders/target_leaders_{position}_{year}.csv", index=False)

    # limit to top 30 of position
    df_pos = df.loc[(df["position"] == position)]
    df_pos = df_pos.sort_values(by="total_receiving_tgt", ascending=False)
    df_pos["rank"] = df_pos["total_receiving_tgt"].rank(ascending=False)
    df_pos = df_pos.loc[df_pos["rank"] < 40]

    # split into single weeks and averages per game
    df_pos.set_index("player", drop=True, inplace=True)
    df_weeks = df_pos.loc[:, [f"week_{i}" for i in weeks]]
    df_avgs = df_pos.loc[:, "receiving_tgt_per_game"]

    # plot stacked horizontal bar plot
    cmap = plt.colormaps["tab20c"]
    colors_dict = dict(zip(range(1, len(weeks) + 1), cmap([i for i in range(len(weeks))])))
    df_weeks.plot.barh(stacked=True, legend=False, figsize=(10, 20), color=cmap([i for i in range(len(weeks))]))

    # patches
    patches = list()
    for week, color in colors_dict.items():
        patch = mp.Patch(color=color, label=f"week {week}")
        patches.append(patch)

    # setup axis
    plt.legend(handles=patches, borderpad=1, fontsize=8)
    plt.title(f"Receiving targets - Top {position}")
    plt.xlabel("received targets")
    plt.tight_layout()
    plt.savefig(f"../reports/target_leaders/target_leaders_{position}_{year}.png")
