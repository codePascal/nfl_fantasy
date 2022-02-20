"""
Analyzes the fantasy scoring relation w.r.t. to statistics such as
passing attempts and receiving targets for a specific position in a
given year.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import utils.fantasy_pros as fp

sns.set_style("whitegrid")

POSITION = "K"
YEAR = 2021

if __name__ == "__main__":
    # get yearly_stats raw
    df = pd.read_csv("../raw/yearly_stats/{pos}/{pos}_{year}.csv".format(pos=POSITION, year=YEAR))
    df = df.dropna()

    # clean raw
    df = fp.clean_stats(df, POSITION)

    # drop unnecessary columns
    df.drop(["rank", "player", "team", "games", "fantasy_points", "rost"], axis=1, inplace=True)

    # plot the correlation heatmap
    plt.figure(figsize=(8, 7))
    plt.title("Scoring correlation for {pos} during season {year}".format(pos=POSITION, year=YEAR))
    sns.heatmap(df.corr(), annot=True, cmap=sns.diverging_palette(0, 250), mask=np.triu(df.corr()))
    plt.tight_layout()
    plt.savefig("../reports/scoring_correlation/correlation_{pos}_{year}.png".format(pos=POSITION, year=YEAR))
    plt.show()
