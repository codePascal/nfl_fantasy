def rank_statistic(df, indicator):
    """
    Sorts data regarding indicator and adds column with rank.

    :param df: data
    :type df: pandas.DataFrame
    :param indicator: column name to rank
    :type indicator: str
    :return: data with ranked indicator
    :rtype: pandas.DataFrame
    """
    df = df.sort_values(by=indicator, ascending=False)
    df[f"{indicator}_rank"] = df[indicator].rank(ascending=False)
    return df



