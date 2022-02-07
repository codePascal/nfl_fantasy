"""
Analyzes expert rankings based on k-means clustering to assign each
player a tier for a fantasy football draft in 2021.

Players are clustered regarding their average ranking of all experts.
One can define if number of tiers should be found via silhouette
scoring (https://en.wikipedia.org/wiki/Silhouette_(clustering)) or if
a fixed number of tiers should be used. Most common are ten tier
rankings in the NFL. Assuming that the league has n teams and m
spots, the top n*m players are taken into consideration.

Source:
    https://www.fantasyfootballdatapros.com/course/section/11
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

sns.set_style('whitegrid')

FIXED_TIER = True
N_TIERS = 10
FIXED_POSITION = True
POSITION = "QB"


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


# load data for 2021 draft
ppr = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ecr/PPR_ECR.csv"
half_ppr = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ecr/HALF_PPR_ECR.csv"
standard = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ecr/STANDARD_ECR.csv"
df = pd.read_csv(ppr, index_col=0)

# league settings
n_teams = 14
n_spots = 16
draft_pool = n_teams * n_spots

# pick top-rated players
df = df.dropna()
df = df.iloc[:draft_pool]

if not FIXED_TIER:
    # find optimal k that maximizes silhouette score
    avgs = list()
    min_cluster = 4
    max_cluster = 34
    for n_clusters in range(min_cluster, max_cluster + 1):
        # pick average expert rank as cluster parameter
        X = df[["Avg"]].values

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
else:
    # run with ten tiers
    k = N_TIERS

# train with optimal number of clusters
labels = KMeans(n_clusters=k, random_state=42).fit_predict(df[["Avg"]].values)

# get tiers
tiers = assign_tiers(labels)
df["Tier"] = tiers

# visualize tier assignment
if FIXED_POSITION:
    df = df.loc[df["Pos"].str.contains(POSITION)]

colors = ['purple', 'magenta', 'red', 'blue', 'orange', 'green', 'salmon', 'yellow', 'black', 'grey', '#3498db',
          '#16a085', '#f4d03f', '#f1948a', '#48c9b0', '#3498db', '#e74c3c', '#d7bde2', '#d0d3d4']
colors = dict(zip(range(1, k+1), colors[:k]))

plt.figure(figsize=(30, 40))
plt.scatter(x=df["Avg"], y=df["Rank"], c="#212f3d", alpha=0.9, s=7)

yticks = list()
for _, row in df.iterrows():
    plt.plot((row["Best"], row["Worst"]), (row["Rank"], row["Rank"]), c=colors.get(row["Tier"], "black"), alpha=0.8)
    yticks.append(row["Player"])

patches = list()
for tier, color in colors.items():
    patch = mp.Patch(color=color, label=f"Tier {tier}")
    patches.append(patch)

plt.legend(handles=patches, borderpad=1, fontsize=12)
plt.xlabel("Average expert rank", fontsize=12)
plt.ylabel("Expert consensus rank", fontsize=12)
plt.yticks(df["Rank"], yticks, fontsize=12)
plt.title("Tiers for 2021 Draft - ECR vs Average Expert Rank", fontsize=12)

plt.gca().invert_yaxis()
plt.savefig("plots/tier_ranking.png")
plt.show()
