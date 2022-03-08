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
