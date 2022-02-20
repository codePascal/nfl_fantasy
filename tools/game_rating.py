"""
Each game is rated as "poor", "quality" or "great" based on the
fantasy points recorded. A player is more reliable for an owner if
it consistently produces fantasy points.

The games are rated based on the average points scored of the top
players per week on this position over the last recent years.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np
import pandas as pd
import scipy.stats
import tqdm

SNAPS_THRESHOLD = 30

position_map = {
    "QB": 0,
    "RB": 1,
    "WR": 2,
    "TE": 3
}

if __name__ == "__main__":
    # load the stats of the recent years
    df = pd.DataFrame()
    yearly = pd.DataFrame()
    for year in range(2016, 2021 + 1):
        chunks = pd.read_csv(f"../preprocessed/stats/offense_summary_{year}.csv", iterator=True, low_memory=False,
                             chunksize=10000)

        # concat the years
        for chunk in tqdm.tqdm(chunks):
            # get necessary data
            chunk = chunk.loc[:, ["position", "fantasy_points", "snaps_percent", "week"]]

            # select only relevant positions
            chunk = chunk[chunk["position"].isin(list(position_map.keys()))]

            # use only if player saw snaps during the game
            chunk = chunk.loc[(chunk["snaps_percent"] > SNAPS_THRESHOLD)]
            chunk.drop(["snaps_percent"], axis=1, inplace=True)

            # drop players that have no fantasy points record
            chunk.dropna(subset=["fantasy_points"], inplace=True)

            # add the year
            chunk["year"] = year
            yearly = pd.concat([yearly, chunk])

        # concat to dataframe
        df = pd.concat([df, yearly])

    # fit a distribution to the fantasy points for each position
    means = list()
    variances = list()
    sigma = list()
    for pos in list(position_map.keys()):
        mean, var = scipy.stats.distributions.norm.fit(df.loc[df["position"] == pos, "fantasy_points"])
        means.append(mean)
        variances.append(var)
        sigma.append(np.sqrt(var))

    # plot the distribution for each position
    fig, axs = plt.subplots(2, 2)
    axs = axs.ravel()
    fig.suptitle("Fantasy points distribution season 2016 to 2021")
    x = np.linspace(-10, 50, 600)
    for i, pos in enumerate(list(position_map.keys())):
        axs[i].hist(df.loc[df["position"] == pos, "fantasy_points"], density=True, bins=20)
        axs[i].plot(x, scipy.stats.distributions.norm.pdf(x, means[i], variances[i]), '-r')
        axs[i].grid()
        axs[i].set_title(pos)
    plt.tight_layout()
    plt.savefig("../reports/game_rating/scoring_distribution_2016to2021.png")

    # load stats from the latest season
    df = pd.read_csv("../preprocessed/stats/offense_summary_2021.csv")
    df = df.loc[:, ["player", "position", "fantasy_points", "team", "opponent", "snaps_percent"]]
    df = df[df["position"].isin(list(position_map.keys()))]

    # drop the BYE week records
    df = df.loc[df["opponent"] != "BYE"]
    df.drop("opponent", axis=1, inplace=True)

    # keep only players that saw snaps
    df = df.loc[df["snaps_percent"] > SNAPS_THRESHOLD]
    df.drop("snaps_percent", axis=1, inplace=True)

    # assign each player if his scoring was poor, quality or great
    for i, player in df.iterrows():
        if player["fantasy_points"] > means[position_map[player["position"]]] + sigma[position_map[player["position"]]]:
            # great game: mu + 2 * sigma < score
            df.at[i, "great_game"] = 1
        elif player["fantasy_points"] < means[position_map[player["position"]]] - sigma[
            position_map[player["position"]]]:
            # poor game: score < mu - 2 * sigma
            df.at[i, "poor_game"] = 1
        else:
            # quality game: mu - 2 * sigma < score < mu + 2 * sigma
            df.at[i, "quality_game"] = 1

    # count the game rating per player
    df = df.groupby(by=["player", "position", "team"]).agg({
        "fantasy_points": np.sum,
        "great_game": np.sum,
        "poor_game": np.sum,
        "quality_game": np.sum})
    df["games"] = df["great_game"] + df["poor_game"] + df["quality_game"]

    # store the dataframe
    df.reset_index(inplace=True)
    df.to_csv("../reports/game_rating/game_rating_2021.csv", index=False)

    for i, pos in enumerate(list(position_map.keys())):
        # plot the summary for top players on each position
        fig, axs = plt.subplots(2, 1, figsize=(10, 15), gridspec_kw={"height_ratios": [1, 10]})

        # plot distribution with definition of game rating
        dist = scipy.stats.distributions.norm.pdf(x, means[i], variances[i])
        axs[0].plot(x, dist, '-r')
        rectangles = {"poor": mp.Rectangle((-10, 0), 10 + means[i] - 2 * sigma[i], max(dist), color="tab:orange",
                                           alpha=0.8),
                      "quality": mp.Rectangle((means[i] - 2 * sigma[i], 0), 4 * sigma[i], max(dist), color="tab:blue",
                                              alpha=0.8),
                      "great": mp.Rectangle((means[i] + 2 * sigma[i], 0), 50 - means[i] - 2 * sigma[i], max(dist),
                                            color="tab:green", alpha=0.8)
                      }
        for rec in rectangles:
            axs[0].add_artist(rectangles[rec])
            rx, ry = rectangles[rec].get_xy()
            cx = rx + rectangles[rec].get_width() / 2.0
            cy = ry + rectangles[rec].get_height() / 2.0
            axs[0].annotate(rec, (cx, cy), color='black', weight="bold", ha="center")

        # plot stacked horizontal bar plot
        df_games = df.copy()
        df_games = df_games.loc[df_games["position"] == pos]

        df_games.sort_values(by="fantasy_points", ascending=False, inplace=True)
        df_games["fantasy_points_rank"] = df_games["fantasy_points"].rank(ascending=False)

        df_games = df_games.loc[df_games["fantasy_points_rank"] < 30]

        df_games = df_games[["player", "poor_game", "quality_game", "great_game"]]
        df_games.set_index("player", inplace=True)

        colors = {"poor_game": "tab:orange",
                  "quality_game": "tab:blue",
                  "great_game": "tab:green"
                  }

        df_games.plot.barh(stacked=True, ax=axs[1], color=colors, legend=False, width=0.2)

        # config figure
        fig.suptitle(f"Game rating regarding normal distribution for {pos}", fontsize=24)
        axs[0].set_xlabel("Fantasy points")
        axs[0].set_title("Normal distribution for scored points from season 2016 to 2021")
        axs[1].set_xlabel("Games")
        axs[1].set_title(f"Game rating for {pos}")

        plt.tight_layout(pad=2.0, w_pad=0.5, h_pad=1.0)
        plt.savefig(f"../reports/game_rating/game_rating_{pos}_2021.png")
