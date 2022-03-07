"""
...
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import sys

from config.mapping import week_map
from src.preprocessing.statistics.stats import Stats


class Leaders:
    def __init__(self, metric, position, year, player=None):
        self.metric = metric
        self.position = position
        self.year = year
        self.player = player

    def get_data(self):
        df = Stats(self.position, self.year).get_accumulated_data()
        df = df.loc[:, ["player", "week", "team", "games", self.metric]]

        df = self.get_weekly_metric(df)
        df = self.accumulate_weekly_metric(df)
        df = self.rank_total(df)
        df = self.rank_per_game(df)

        return df

    def get_weekly_metric(self, df):
        for week in range(1, week_map[self.year] + 1):
            df[f"week_{week}"] = df.loc[df["week"] == week].loc[:, self.metric]
        df.drop(["week", self.metric], axis=1, inplace=True)
        return df

    def accumulate_weekly_metric(self, df):
        if week_map[self.year] == 17:
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
        elif week_map[self.year] == 18:
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
        return df

    def rank_total(self, df):
        df[f"total_{self.metric}"] = df.loc[:, [f"week_{i}" for i in range(1, week_map[self.year] + 1)]].sum(axis=1)
        df = df.sort_values(by=f"total_{self.metric}", ascending=False)
        df[f"total_{self.metric}_rank"] = df[f"total_{self.metric}"].rank(ascending=False)
        return df

    def rank_per_game(self, df):
        df[f"{self.metric}_per_game"] = df.loc[:, f"total_{self.metric}"] / df.loc[:, "games"]
        df = df.sort_values(by=f"{self.metric}_per_game", ascending=False)
        df[f"{self.metric}_per_game_rank"] = df[f"{self.metric}_per_game"].rank(ascending=False)
        return df

    def plot_leaders_total(self, n=20):
        df = self.get_data()

        df = df.loc[df[f"total_{self.metric}_rank"] < n]
        df = df.sort_values(by=f"total_{self.metric}", ascending=False)

        df.set_index("player", drop=True, inplace=True)
        df = df.loc[:, [f"week_{i}" for i in range(1, week_map[self.year] + 1)]]

        self.plot_stacked_barplot(df, f"Top {self.position} for total {self.metric} in {self.year}")

    def plot_leaders_average(self, n=20):
        df = self.get_data()

        df = df.loc[df[f"{self.metric}_per_game_rank"] < n]
        df = df.sort_values(by=f"{self.metric}_per_game_rank", ascending=False)

        df.set_index("player", drop=True, inplace=True)
        df = df.loc[:, [f"week_{i}" for i in range(1, week_map[self.year] + 1)]]

        self.plot_stacked_barplot(df, f"Top {self.position} for {self.metric} per game in {self.year}")

    def plot_stacked_barplot(self, df, title):
        # plot stacked horizontal bar plot
        cmap = plt.colormaps["tab20c"]
        colors_dict = dict(zip(range(1, week_map[self.year] + 1), cmap([i for i in range(week_map[self.year])])))
        df.plot.barh(stacked=True, legend=False, figsize=(10, 20),
                     color=cmap([i for i in range(week_map[self.year])]))

        # patches
        patches = list()
        for week, color in colors_dict.items():
            patch = mp.Patch(color=color, label=f"week {week}")
            patches.append(patch)

        # setup axis
        plt.legend(handles=patches, borderpad=1, fontsize=8)
        plt.title(title)
        plt.xlabel(self.metric)
        plt.tight_layout()
        plt.show()

    def get_player(self):
        df = self.get_data()
        if self.player:
            return df.loc[df["player"] == self.player, :].squeeze()
        else:
            sys.exit("No player specified.")


if __name__ == "__main__":
    Leaders("rushing_td", "RB", 2021).plot_leaders_total()
    Leaders("rushing_td", "RB", 2021).plot_leaders_average()

