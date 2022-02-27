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

from src.preprocessing.statistics.statistics import Statistics

SNAPS_THRESHOLD = 30


if __name__ == "__main__":
    # position
    position = "WR"

    # load the stats of the recent years
    df = pd.DataFrame()
    yearly = pd.DataFrame()
    for year in range(2016, 2021 + 1):
        # load summary of offense
        yearly = Statistics(position, year).get_accumulated_data()

        # get necessary data
        yearly = yearly.loc[:, ["fantasy_points", "snaps_percent", "week"]]

        # use only if player saw snaps during the game
        yearly = yearly.loc[(yearly["snaps_percent"] > SNAPS_THRESHOLD)]
        yearly.drop(["snaps_percent"], axis=1, inplace=True)

        # drop players that have no fantasy points record
        yearly.dropna(inplace=True)

        # concat to dataframe
        df = pd.concat([df, yearly])

    # fit a distribution to the fantasy points for each position
    mean, var = scipy.stats.distributions.norm.fit(df.loc[:, "fantasy_points"])
    sigma = np.sqrt(var)

    # load stats from the latest season
    df = Statistics(position, 2021).get_accumulated_data()
    df = df.loc[:, ["player", "fantasy_points", "team", "opponent", "snaps_percent"]]

    # drop the BYE week records
    df = df.loc[df["opponent"] != "BYE"]
    df.drop("opponent", axis=1, inplace=True)

    # keep only players that saw snaps
    df = df.loc[df["snaps_percent"] > SNAPS_THRESHOLD]
    df.drop("snaps_percent", axis=1, inplace=True)

    # assign each player if his scoring was poor, quality or great
    for i, player in df.iterrows():
        if player["fantasy_points"] > mean + 2 * sigma:
            # great game: mu + 2 * sigma < score
            df.at[i, "great_game"] = 1
        elif player["fantasy_points"] < mean - 2 * sigma:
            # poor game: score < mu - 2 * sigma
            df.at[i, "poor_game"] = 1
        else:
            # quality game: mu - 2 * sigma < score < mu + 2 * sigma
            df.at[i, "quality_game"] = 1

    # count the game rating per player
    df = df.groupby(by=["player", "team"]).agg({
        "fantasy_points": np.sum,
        "great_game": np.sum,
        "poor_game": np.sum,
        "quality_game": np.sum})
    df["games"] = df["great_game"] + df["poor_game"] + df["quality_game"]

    # store the dataframe
    df.reset_index(inplace=True)
    df.to_csv(f"../reports/game_rating/game_rating_{position}_2021.csv", index=False)

    # plot the summary for top players on each position
    fig, axs = plt.subplots(2, 1, figsize=(10, 15), gridspec_kw={"height_ratios": [1, 10]})

    # plot distribution with definition of game rating
    x = np.linspace(-10, 50, 600)
    dist = scipy.stats.distributions.norm.pdf(x, mean, var)
    axs[0].plot(x, dist, '-r')
    rectangles = {"poor": mp.Rectangle((-10, 0), 10 + mean - 2 * sigma, max(dist), color="tab:orange",
                                       alpha=0.8),
                  "quality": mp.Rectangle((mean - 2 * sigma, 0), 4 * sigma, max(dist), color="tab:blue",
                                          alpha=0.8),
                  "great": mp.Rectangle((mean + 2 * sigma, 0), 50 - mean - 2 * sigma, max(dist),
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
    fig.suptitle(f"Game rating regarding normal distribution for {position}", fontsize=24)
    axs[0].set_xlabel("Fantasy points")
    axs[0].set_title("Normal distribution for scored points from season 2016 to 2021")
    axs[1].set_xlabel("Games")
    axs[1].set_title(f"Game rating for {position}")

    plt.tight_layout(pad=2.0, w_pad=0.5, h_pad=1.0)
    plt.savefig(f"../reports/game_rating/game_rating_{position}_2021.png")
