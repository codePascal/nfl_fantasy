def calculate_standard_fantasy_points(player):
    """
    Calculates fantasy points with standard scoring scheme.

    :param player: stats of QB
    :type player: pandas.Series
    :return: standard fantasy points
    :rtype: float
    """
    if player["position"] == "QB":
        return 6 * player["rushing_td"] + 0.1 * player["rushing_yds"] + 4 * player["passing_td"] + 1 / 25 * player[
            "passing_yds"] + (-1) * player["passing_int"] + (-2) * player["lst"]
    elif player["position"] == "RB" or player["position"] == "TE" or player["position"] == "WR":
        return 6 * (player["rushing_td"] + player["receiving_td"]) + 0.1 * (
                player["rushing_yds"] + player["receiving_yds"]) + (-2) * player["lst"]


def calculate_halfppr_fantasy_points(player):
    """
    Calculates fantasy points with half-PPR scoring scheme.

    :param player: stats of QB
    :type player: pandas.Series
    :return: half-PPR fantasy points
    :rtype: float
    """
    if player["position"] == "QB":
        return 6 * player["rushing_td"] + 0.1 * player["rushing_yds"] + 4 * player["passing_td"] + 1 / 25 * player[
            "passing_yds"] + (-1) * player["passing_int"] + (-2) * player["lst"]
    elif player["position"] == "RB" or player["position"] == "TE" or player["position"] == "WR":
        return 6 * (player["rushing_td"] + player["receiving_td"]) + 0.1 * (
                player["rushing_yds"] + player["receiving_yds"]) + 0.5 * player["receiving_rec"] + (-2) * player[
                   "lst"]


def calculate_ppr_fantasy_points(player):
    """
    Calculates fantasy points with PPR scoring scheme.

    :param player: stats of QB
    :type player: pandas.Series
    :return: PPR fantasy points
    :rtype: float
    """
    if player["position"] == "QB":
        return 6 * player["rushing_td"] + 0.1 * player["rushing_yds"] + 4 * player["passing_td"] + 1 / 25 * player[
            "passing_yds"] + (-1) * player["passing_int"] + (-2) * player["lst"]
    elif player["position"] == "RB" or player["position"] == "TE" or player["position"] == "WR":
        return 6 * (player["rushing_td"] + player["receiving_td"]) + 0.1 * (
                player["rushing_yds"] + player["receiving_yds"]) + 1.0 * player["receiving_rec"] + (-2) * player[
                   "lst"]
