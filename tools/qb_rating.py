"""
Returns the ranking of QB in the NFL based on metric introduced back
in early 1970s by Don Smith, Seymour Siwoff and Don Weiss.

While it is a very complicated measure, it also does not respect the
recent development in terms of QB efficiency. Recent famous QB such
as Patrick Mahomes and Joe Burrow developed a style that leads to
more rushing yards by a QB instead of just throwing.
"""
import matplotlib.pyplot as plt
import seaborn as sns


import utils.fantasy_pros as fp
import utils.data_handling as dh

sns.set_style("whitegrid")

YEAR = 2020


def get_qb_rating(player):
    """
    Calculates the rating of a QB as introduced in the early 1970s by
    Don Smith, Seymour Siwoff and Don Weiss.

    :param player: stats of QB
    :type player: pandas.Series
    :return: QB rating
    :rtype: float
    """
    comp = player["passing_cmp"]
    pass_yds = player["passing_yds"]
    pass_td = player["passing_td"]
    ints = player["passing_int"]
    pass_att = player["passing_att"]

    if not pass_att == 0:
        return 100 / 6 * ((comp / pass_att - 0.3) / 0.2 + (pass_yds / pass_att - 3) / 4 + (pass_td / pass_att) / 0.05 +
                          (0.095 - ints / pass_att) / 0.04)
    else:
        return 0


if __name__ == "__main__":
    # load data
    yearly = dh.read_csv_file("../data/yearly_stats/QB/QB_{}.csv".format(YEAR))
    yearly = yearly.dropna()

    # clean up the data
    yearly = fp.clean_stats_qb(yearly)

    # get rankings
    yearly["rating"] = yearly.apply(get_qb_rating, axis=1)

    # use only QB that have played number of games
    games_threshold = 10
    yearly = yearly.loc[(yearly["misc_g"] > games_threshold), :]

    # get the rank of the rating
    yearly["rating_rank"] = yearly["rating"].rank(ascending=False)
    yearly = yearly.astype({"rating_rank": int})

    # plot the rating vs fantasy points
    yearly.rename(columns={"misc_fpts": "fantasy points"}, inplace=True)
    plt.figure()
    plt.title("QB rating vs. fantasy points scored in {}".format(YEAR))
    sns.scatterplot(x="rating", y="fantasy points", data=yearly)
    plt.show()
