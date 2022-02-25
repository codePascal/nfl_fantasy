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
"""
import matplotlib.pyplot as plt
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from pmdarima.arima import auto_arima

from src.preprocessing.stats import Stats


# noinspection PyTypeChecker
def test_stationarity(series):
    result = dict(zip(['adf', "pvalue", "usedlag", "nobs", "critical values", "icbest"], adfuller(series)))
    if result["pvalue"] > 0.05:
        return False
    return True


# define selector and player
selector = "passing_att"
player = "Aaron Rodgers"

# load weekly stats for given year range
df = pd.DataFrame()
for year in range(2010, 2021 + 1):
    df = pd.concat([df, Stats(year).get_accumulated_data()])

# get stats for player only
df = df.loc[df["player"] == player]

# split to training and test
df_train = df.loc[df["year"] < 2021, [selector]].reset_index(drop=True)
df_test = df.loc[df["year"] == 2021, [selector]].reset_index(drop=True)

# check for stationarity of raw time series
m = 17
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
prediction = stepwise_model.predict(n_periods=18)

# summarize and plot
df_test["prediction"] = prediction
df_test.plot()
plt.show()
