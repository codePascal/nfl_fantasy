"""
Code source:
    https://www.fantasyfootballdatapros.com/course/section/10
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

sns.set_style("whitegrid")

if __name__ == "__main__":
    # load the cleaned raw
    df = pd.read_csv("data_cleaned.csv").iloc[:, 1:]

    # summarize the raw
    df = df.groupby(['player_id', 'tm', 'player', 'pos', 'season'], as_index=False).agg({
        'offensive_snapcount': np.sum,
        'offensive_snapcount_percentage': np.mean,
        'passing_rating': np.mean,
        'passing_yds': np.sum,
        'passing_td': np.sum,
        'passing_att': np.sum,
        'receiving_yds': np.sum,
        'receiving_td': np.sum,
        'receiving_rec': np.sum,
        'receiving_tar': np.sum,
        'rushing_att': np.sum,
        'standard_fantasy_points': np.sum,
        'ppr_fantasy_points': np.sum,
        'half_ppr_fantasy_points': np.sum
    })

    # keep only seasons where weekly_snapcounts are recorded
    df = df.loc[(df["season"]) >= 2012]

    # features to store
    lag_features = ['rushing_att',
                    'receiving_tar',
                    'offensive_snapcount',
                    'offensive_snapcount_percentage',
                    'ppr_fantasy_points',
                    'passing_rating',
                    'passing_att',
                    'passing_td']

    # get the features for the last five years
    for lag in range(1, 6):
        shifted = df.groupby("player_id").shift(lag)

        for feature in lag_features:
            df[f"lag_{feature}_{lag}"] = shifted[feature]
    df = df.fillna(-1)

    # consider WR only
    wr_df = df.loc[(df["pos"] == "WR")]

    # drop 2019 season
    wr_df = wr_df.loc[(wr_df["season"] < 2019)]

    # in general, hard to predict players with low utilization
    snapcounts_threshold = 50
    wr_df = wr_df.loc[(wr_df["lag_offensive_snapcount_1"] > snapcounts_threshold)]

    # plot residuals
    sns.residplot(x=wr_df["lag_offensive_snapcount_1"], y=wr_df["ppr_fantasy_points"])
    # plt.show()

    # prepare training raw
    X_data = wr_df[["lag_receiving_tar_1", "lag_offensive_snapcount_1", "lag_ppr_fantasy_points_1"]].values
    y_data = wr_df["ppr_fantasy_points"].values

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=10)

    # train model
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # predict
    y_pred = lr.predict(X_test)

    # compare
    mae = mean_absolute_error(y_pred, y_test)

    # predict 2020 fantasy points based on 2019 stats
    wr_df_pred = df.loc[
        (df['pos'] == 'WR') & (df['offensive_snapcount'] > 50) & (df['season'] == 2019),
        ['player', 'receiving_tar', 'offensive_snapcount', 'ppr_fantasy_points']
    ]

    wr_df_pred['predicted_2020'] = lr.predict(
        wr_df_pred[['receiving_tar', 'offensive_snapcount', 'ppr_fantasy_points']].values
    )

    # check result
    wr_df_pred = wr_df_pred.sort_values(by='predicted_2020', ascending=False)
    pd.set_option("display.max_rows", None)
    print(wr_df_pred[["player", "predicted_2020"]])
