"""
Preliminary for offense only.

- Train on data from 2016 to 2020
- Test on data from 2021
- Compare projections to fantasy pros projections

- Feature selection: Correlation of offense stats, snapcounts, defense stats
- Weekly stats -> years * weeks
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, max_error

import src.preprocessing.projections.projections as projections
import src.preprocessing.statistics.summary.offense as offense


def fix_home(home):
    if home:
        return 1
    else:
        return 0


def map_names(names):
    unique_names = dict()
    id_ = 0
    for name in names:
        if name not in unique_names.keys():
            unique_names[name] = id_
            id_ += 1
    return unique_names


def fix_names(names, ids):
    return [int(ids[name]) if name in ids.keys() else np.nan for name in names]


if __name__ == "__main__":
    # position, fix
    position = "QB"

    # player
    player = "Aaron Rodgers"

    # load complete data
    df = pd.DataFrame()
    for year in range(2016, 2021 + 1):
        # load yearly data
        yearly = offense.get_offense_stats_summary(year)

        # get only relevant position and drop bye week records and if player did not play
        yearly = yearly.loc[(yearly["position"] == position) & (yearly["opponent"] != "BYE") & (yearly["games"] == 1)]
        yearly.drop("games", axis=1, inplace=True)

        # change booleans to ints for home game column
        yearly["home"] = yearly["home"].apply(fix_home)

        # drop columns not relevant for position QB
        yearly.drop(["rost", 'rushing_ya', 'rushing_lg', 'rushing_20p', 'receiving_rec', 'receiving_tgt',
                     'receiving_yds', 'receiving_yr', 'receiving_td', 'receiving_lg', 'receiving_20p'],
                    axis=1, inplace=True)

        # drop nans in row entries
        yearly.dropna(axis=0, inplace=True)

        # concat
        df = pd.concat([df, yearly])

    # add fantasy points predictions from fantasy pros
    df_predictions = projections.get_accumulated_projections_weekly(2021, "QB")
    df_predictions["year"] = 2021  # TODO fixme in projections loader
    df_predictions = df_predictions.loc[:, ["player", "week", "year", "position", "fantasy_points"]]
    df_predictions.rename(columns={"fantasy_points": "fantasy_points_pred_fantasypros"}, inplace=True)
    df = pd.merge(df, df_predictions, how="outer", on=["player", "week", "position", "year"])

    # drop players that have no fantasy points recorded
    df = df[df["fantasy_points"].notna()]

    # drop position
    df.drop("position", axis=1, inplace=True)

    # fix team and opponents
    team_ids = map_names(df.team.unique())
    df["team_id"] = fix_names(df["team"].to_list(), team_ids)
    df["opponent_id"] = fix_names(df["opponent"].to_list(), team_ids)

    # fix names
    name_ids = map_names(df.player.unique())
    df["player_id"] = fix_names(df["player"].to_list(), name_ids)

    # split into features and targets
    df_features = df.drop(["fantasy_points", "fantasy_points_pred_fantasypros", "player", "team", "opponent"], axis=1)
    df_targets = df.loc[:, ["player", "player_id", "week", "year", "fantasy_points", "fantasy_points_pred_fantasypros"]]

    # get correlation heatmap of features
    sns.heatmap(df.corr(), annot=True)
    # plt.tight_layout()
    # plt.show()

    # drop a feature if absolute correlation with another one is higher than a threshold
    threshold = 0.9
    corr = df_features.corr().abs()
    upper_tri = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [col for col in upper_tri.columns if any(upper_tri[col] > threshold)]
    df_features = df_features.drop([col for col in to_drop], axis=1)

    # use stats until second last season to train
    X_train = df_features.loc[df_features["year"] < 2021]
    y_train = df_targets.loc[df_features["year"] < 2021].drop(
        ["player", "player_id", "week", "year", "fantasy_points_pred_fantasypros"], axis=1)

    # use recent season stats for testing
    X_test = df_features.loc[df_features["year"] == 2021]
    y_targets = df_targets.loc[df_targets["year"] == 2021]

    # linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # add predicted points to targets
    y_pred = [elem[0] for elem in y_pred]
    y_targets["fantasy_points_predicted"] = y_pred

    # predictions from fantasy pros have nan sometimes (if retired)
    y_targets.dropna(axis=0, inplace=True)

    # observe prediction accuracy
    rmse_fp = mean_squared_error(y_targets["fantasy_points"].to_list(),
                                 y_targets["fantasy_points_pred_fantasypros"].to_list())
    rmse_pred = mean_squared_error(y_targets["fantasy_points"].to_list(),
                                   y_targets["fantasy_points_predicted"].to_list())

    print("Mean squared error for fantasy pros predictions:", round(rmse_fp, 3))
    print("Mean squared error for linear regression model:", round(rmse_pred, 3))

    max_fp = max_error(y_targets["fantasy_points"].to_list(), y_targets["fantasy_points_pred_fantasypros"].to_list())
    max_pred = max_error(y_targets["fantasy_points"].to_list(), y_targets["fantasy_points_predicted"].to_list())

    print("Maximum error for fantasy pros predictions:", round(max_fp, 3))
    print("Maximum error for linear regression model:", round(max_pred, 3))

