"""
Implements a uni-variate ARIMA (AutoRegressive Integrated Moving
Average) model to predict performance metrics for players.

Description ARIMA
AR: time series is regressed on its own lagged values
I: differencing to achieve stationarity
MA: regression error is a linear combination of error terms

Arguments ARIMA
order = (p, d, q)
    p: number of lag observations
    d: number of differencing till stationarity
    q: size of moving average window

seasonal_order = (P, D, Q, m)
    P: number of seasonal lag observations
    D: number of differencing seasonal observations till stationarity
    Q: size of seasonal moving average window
    m: number of observations per season

The current implementation only supports to evaluate QB veterans, e.g.
QB that have played in the recent years, say from 2016 on.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from pmdarima.arima import auto_arima

from src.preprocessing.statistics.statistics import Statistics

SHOW_PLOT = True


# noinspection PyTypeChecker
def test_stationarity(series):
    result = dict(zip(['adf', "pvalue", "usedlag", "nobs", "critical values", "icbest"], adfuller(series)))
    if result["pvalue"] > 0.05:
        return False
    return True


def predict_performance(df_train, selector, n_samples):
    # check for stationarity of raw time series
    m = 16
    d = 0
    df_train["0_difference"] = df_train[selector]
    while True:
        if test_stationarity(df_train[f"{d}_difference"].dropna()):
            break
        df_train[f"{d + 1}_difference"] = df_train[f"{d}_difference"] - df_train[f"{d}_difference"].shift(1)
        d += 1

    # check for stationarity of seasonal data
    D = 0
    df_train["0_seasonal_difference"] = df_train["0_difference"] - df_train["0_difference"].shift(m)
    while True:
        if test_stationarity(df_train[f"{D}_seasonal_difference"].dropna()):
            break
        df_train[f"{D + 1}_seasonal_difference"] = df_train[f"{D}_seasonal_difference"] - df_train[
            f"{D}_seasonal_difference"].shift(1)
        D += 1

    if SHOW_PLOT:
        # check auto-correlation and partial auto-correlation for time series and seasonal data
        fig, axs = plt.subplots(2, 2)
        axs = axs.ravel()
        plot_acf(df_train[f"{d}_difference"], ax=axs[0], title=f"AC Difference (d = {d})")
        plot_pacf(df_train[f"{d}_difference"], method="ywm", ax=axs[1], title=f"PAC Difference (d = {d})")
        plot_acf(df_train[f"{D}_seasonal_difference"].dropna(), ax=axs[2], title=f"AC Seasonal Difference (D = {D})")
        plot_pacf(df_train[f"{D}_seasonal_difference"].dropna(), method="ywm", ax=axs[3],
                  title=f"PAC Seasonal Difference (D = {D})")
        plt.tight_layout()
        plt.show()

    # reset to only raw time series
    df_train = df_train.loc[:, selector]

    # detect optimal tuning with auto arima
    stepwise_model = auto_arima(df_train, d=d, D=D, m=m, start_p=0, start_q=0, max_p=10, max_q=10, seasonal=True,
                                start_P=0, start_Q=0, trace=True, error_action="ignore", suppress_warnings=True,
                                stepwise=True)
    print(stepwise_model.aic())

    # fit the model
    stepwise_model.fit(df_train)

    # predict, NFL season 2021 had 18 weeks (thanks...)
    return stepwise_model.predict(n_periods=n_samples)


def calculate_fantasy_points(series):
    pass_yds = series["passing_yds"]
    pass_int = series["passing_int"]
    pass_td = series["passing_td"]
    rush_yds = series["rushing_yds"]
    rush_td = series["rushing_td"]
    fumbles_lost = series["lst"]
    return 1 / 25 * pass_yds + (-1) * pass_int + 4 * pass_td + 0.1 * rush_yds + 6 * rush_td + (-2) * fumbles_lost


if __name__ == "__main__":
    # define selector and player (here for QB)
    selectors = ["passing_yds", "passing_int", "passing_td", "rushing_yds", "rushing_td", "lst"]
    player = "Aaron Rodgers"
    position = "QB"
    year_to_pred = 2021

    # load weekly stats for given year range
    df = pd.DataFrame()
    for year in range(2010, year_to_pred + 1):
        df = pd.concat([df, Statistics(position, year).get_accumulated_data()])

    # get stats where player played
    df_player = df.loc[(df["player"] == player) & (df["games"] != 0)].reset_index(drop=True)

    # get prediction for each performance metric
    df_pred = pd.DataFrame(np.nan, index=selectors, columns=["actual", "predicted"])
    for selector in selectors:
        if SHOW_PLOT:
            # plot the selected data
            df_player[selector].plot()
            plt.show()

        # split to training and test
        df_train = df_player.loc[df_player["year"] < year_to_pred, [selector]].reset_index(drop=True)
        df_test = df_player.loc[df_player["year"] == year_to_pred, [selector]].reset_index(drop=True)

        # predict
        # TODO add test if data is sufficient to predict
        #  "ValueError: sample size is too short to use selected regression component"
        #  > 32
        print(len(df_train))
        df_test[f"{selector}_pred"] = predict_performance(df_train, selector, df_test.shape[0])
        df_pred.loc[selector, "actual"] = df_test[selector].sum()
        df_pred.loc[selector, "predicted"] = df_test[f"{selector}_pred"].sum()

    # calculate fantasy points
    print(calculate_fantasy_points(df_pred.loc[:, "actual"]))
    print(calculate_fantasy_points(df_pred.loc[:, "predicted"]))
