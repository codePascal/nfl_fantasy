"""
Analyzes the fantasy scoring relation w.r.t. to statistics such as
passing attempts and receiving targets for a specific position in a
given year.
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys

import utils.fantasy_pros as fp
import utils.data_handling as dh

sns.set_style("whitegrid")

POSITION = "K"
YEAR = 2021

if __name__ == "__main__":
    # get yearly_stats data
    df = dh.read_csv_file("../data/yearly_stats/{pos}/{pos}_{year}.csv".format(pos=POSITION, year=YEAR))
    df = df.dropna()

    # clean data
    if POSITION == "QB":
        df = fp.clean_stats_qb(df)
    elif POSITION == "RB":
        df = fp.clean_stats_rb(df)
    elif POSITION == "TE":
        df = fp.clean_stats_te(df)
    elif POSITION == "WR":
        df = fp.clean_stats_wr(df)
    elif POSITION == "DST":
        df = fp.clean_stats_def(df)
    elif POSITION == "K":
        df = fp.clean_stats_k(df)
    else:
        sys.exit("Position not implemented.")

    # drop unnecessary columns
    df.drop(["rank", "player", "team", "misc_g", "misc_fpts", "misc_rost"], axis=1, inplace=True)

    # plot the correlation heatmap
    plt.figure(figsize=(8, 7))
    plt.title("Scoring correlation for {pos} during season {year}".format(pos=POSITION, year=YEAR))
    sns.heatmap(df.corr(), annot=True, cmap=sns.diverging_palette(0, 250), mask=np.triu(df.corr()))
    plt.tight_layout()
    plt.savefig("../plots/scoring_correlation/correlation_{pos}_{year}.png".format(pos=POSITION, year=YEAR))
    plt.show()
