"""
...
"""
import pandas as pd
import matplotlib.pyplot as plt

from src.preprocessing.statistics.statistics import Statistics
from src.preprocessing.statistics.projections import Projections


def compare_metric_prediction(position, year, selector):
    stats = Statistics(position, year).get_accumulated_data()
    pred = Projections(position, year).get_accumulated_data()

    stats = stats.loc[:, ["player", "week", selector]]
    pred = pred.loc[:, ["player", "week", selector]]

    summary = pd.merge(stats, pred, how="inner", on=["player", "week"])
    summary.rename(columns={f"{selector}_x": "actual", f"{selector}_y": "prediction"}, inplace=True)
    summary["actual-prediction"] = summary["actual"] - summary["prediction"]

    summary.loc[:, ["actual", "actual-prediction"]].hist(bins=20)
    plt.show()


if __name__ == "__main__":
    compare_metric_prediction("QB", 2021, "passing_yds")
