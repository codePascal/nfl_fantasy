import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, OrdinalEncoder, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline

from src.preprocessing.statistics.statistics import Statistics

if __name__ == "__main__":
    # specify requirements
    player = "Matt Ryan"
    position = "QB"
    year_to_pred = 2021

    # load all present data
    df = pd.DataFrame()
    for year in range(2009, year_to_pred + 1):
        df = pd.concat([df, Statistics(position, year).get_accumulated_data()])

    # clean
    df = df.loc[df["player"] == player].reset_index(drop=True)
    df.drop(["player", "position", "games", "team", "week"], axis=1, inplace=True)

    # make categorical data numeric
    enc = LabelEncoder()
    df["opponent"] = enc.fit_transform(df["opponent"])

    # split
    df_train = df.loc[df["year"] < 2021].drop("year", axis=1)
    df_test = df.loc[df["year"] == 2021].drop("year", axis=1)

    # define labels, categorical features and numerical ones
    cols = df_train.columns.to_list()
    labels = ['passing_cmp', 'passing_att', 'passing_cmppct', 'passing_yds', 'passing_avg', 'passing_td', 'passing_int',
              'sacked', 'rushing_att', 'rushing_yds', 'rushing_td', 'lst', 'fantasy_points']
    cat_features = ["home", "opponent"]
    num_features = list(set(cols) - set(labels + cat_features))

    # specify target to predict
    label = labels[-1]

    # pick only features with correlation between 0.1 and 0.9 with target
    data = df_train.loc[:, num_features + cat_features + [label]]
    data_corr = data.corr().abs().iloc[-1, :-1]
    to_drop = [col for col in data_corr.index if data_corr[col] < 0.1 or data_corr[col] > 0.9]
    data.drop(to_drop, axis=1, inplace=True)
    sns.heatmap(data.corr())
    plt.tight_layout()
    # plt.show()

    # drop highly correlated features
    data.drop(label, axis=1, inplace=True)
    data_corr = data.corr().abs()
    upper_tri = data_corr.where(np.triu(np.ones(data_corr.shape), k=1).astype(bool))
    to_drop = [col for col in upper_tri.columns if any(upper_tri[col] > 0.9)]
    data.drop(to_drop, axis=1, inplace=True)
    sns.heatmap(data.corr())
    plt.tight_layout()
    # plt.show()

    # update numerical features
    num_features = list(set(data.columns.to_list()) - set(cat_features + labels))

    # split into train and test data
    X_train = df_train.loc[:, num_features + cat_features]
    y_train = df_train.loc[:, label]
    X_test = df_test.loc[:, num_features + cat_features]
    y_test = df_test.loc[:, label]

    # create pipeline
    num_transformer = StandardScaler()
    preprocessor = ColumnTransformer(
        transformers=[("num", num_transformer, num_features)]
    )
    clf = Pipeline(
        steps=[("preprocessor", preprocessor), ("model", SVR(kernel='poly', verbose=True))]
    )

    # train and predict
    clf.fit(X_train, y_train)
    print("model score: %.3f" % clf.score(X_test, y_test))
    y_pred = clf.predict(X_test)
    print("MSE:", mean_squared_error(y_test, y_pred))
    print(y_pred, y_test)
