"""
Analyzes the fantasy scoring relation w.r.t. to statistics such as
passing attempts and receiving targets for a specific position in a
given year.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.loader.stats import YearlyStats


sns.set_style("whitegrid")


if __name__ == "__main__":
    # position and year
    positions = ["DST", "K", "QB", "RB", "TE", "WR"]
    year = 2021

    for position in positions:
        # get yearly_stats raw
        df = YearlyStats(position, year).get_data()

        # drop unnecessary columns
        df.drop(["rank", "player", "team", "games", "fantasy_points", "rost", "year"], axis=1, inplace=True)

        # plot the correlation heatmap
        plt.figure(figsize=(8, 7))
        plt.title("Scoring correlation for {pos} during season {year}".format(pos=position, year=year))
        sns.heatmap(df.corr(), annot=True, cmap=sns.diverging_palette(0, 250), mask=np.triu(df.corr()))
        plt.tight_layout()
        plt.savefig("../reports/scoring_correlation/correlation_{pos}_{year}.png".format(pos=position, year=year))
        plt.show()
