"""
Analyzes the ECR for the fantasy draft based on average rating of
many experts. Using clustering, the number of tier rankings is
determined and assigned to each player.
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

sns.set_style('whitegrid')

POSITIONS = ["DST", "K", "QB", "RB", "TE", "WR"]
LEAGUE_SIZE = 14
YEAR = 2022

roster = {
    "ROSTER": 16,
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "K": 1,
    "DST": 1,
    "FLEX": 1,
    "BN": 7
}


def assign_tiers(labels):
    """
    Map the labels to fantasy football tiers.

    :param labels: trained labels
    :type labels: list of ints
    :return: tier of player
    :rtype: list of ints
    """
    unique_labels = list()
    tiers = list()

    # check for each label which tier it is
    for label in labels:
        # assign unique label
        if label not in unique_labels:
            unique_labels.append(label)

        # players are ranked in descending order
        tiers.append(len(set(unique_labels)))

    return tiers


if __name__ == "__main__":
    # load ECR for draft
    df = pd.read_csv(f"../raw/ECR/ecr_{YEAR}.csv", index_col=0)
    df.reset_index(inplace=True)

    # make plot for each position only
    for position in POSITIONS:
        # select only defined position
        df_pos = df.loc[df["POS"].str.contains(position), :]

        # pick only top players on position
        pool = 0
        if position == "DST":
            pool = 2 * LEAGUE_SIZE
        elif position == "K":
            pool = 2 * LEAGUE_SIZE
        elif position == "QB":
            pool = 2 * LEAGUE_SIZE
        elif position == "RB":
            pool = 4 * LEAGUE_SIZE
        elif position == "TE":
            pool = 2 * LEAGUE_SIZE
        elif position == "WR":
            pool = 4 * LEAGUE_SIZE
        df_pos = df_pos.iloc[:pool, :]

        # find optimal k that maximizes silhouette score
        avgs = list()
        if position == "DST" or position == "K":
            min_cluster = 4
        else:
            min_cluster = 8
        max_cluster = 25
        for n_clusters in range(min_cluster, max_cluster + 1):
            # pick average expert rank as cluster parameter
            X = df_pos[["AVG."]].values

            # train model
            labels = KMeans(n_clusters=int(n_clusters)).fit_predict(X)

            # get silhouette score
            silhouette_avg = silhouette_score(X, labels)
            avgs.append(silhouette_avg)

        # plot silhouette score for different number of clusters
        plt.plot(np.arange(min_cluster, max_cluster + 1, 1), avgs)
        plt.xlabel("k")
        plt.ylabel("Silhouette score")
        plt.show()

        # get optimal k
        k = avgs.index(max(avgs)) + min_cluster

        # train with optimal number of clusters
        labels = KMeans(n_clusters=k, random_state=42).fit_predict(df_pos[["AVG."]].values)
        tiers = assign_tiers(labels)
        df_pos["TIERS"] = tiers

        # visualize tier assignment
        colors = ['purple', 'magenta', 'red', 'blue', 'orange', 'green', 'salmon', 'yellow', 'black', 'grey', '#3498db',
                  '#16a085', '#f4d03f', '#f1948a', '#48c9b0', '#3498db', '#e74c3c', '#d7bde2', '#d0d3d4']
        colors = dict(zip(range(1, k+1), colors[:k]))
        plt.figure(figsize=(20, 40))
        plt.scatter(x=df_pos["AVG."], y=df_pos["RK"], c="#212f3d", alpha=0.9, s=7)

        # add each players name and experts ranks
        yticks = list()
        for _, row in df_pos.iterrows():
            plt.plot((row["BEST"], row["WORST"]), (row["RK"], row["RK"]), c=colors.get(row["TIERS"], "black"),
                     alpha=0.8)
            yticks.append(row["PLAYER NAME"])

        # add tier and color for specific tier
        patches = list()
        for tier, color in colors.items():
            patch = mp.Patch(color=color, label=f"Tier {tier}")
            patches.append(patch)

        # setup
        plt.legend(handles=patches, borderpad=1, fontsize=10)
        plt.xlabel("Average expert rank", fontsize=10)
        plt.ylabel("Expert consensus rank", fontsize=10)
        plt.yticks(df_pos["RK"], yticks, fontsize=8)
        plt.title(f"{position} Tiers for {YEAR} Draft - ECR vs Average Expert Rank", fontsize=12)
        plt.gca().invert_yaxis()
        plt.tight_layout()

        # save plot and data
        df_pos.to_csv(f"../reports/draft_ranking/tier_ranking_{position}_{YEAR}.csv", index=False)
        plt.savefig(f"../reports/draft_ranking/tier_ranking_{position}_{YEAR}.png")
