
import pandas as pd

from abc import ABC

from src.models.models import Models
from src.preprocessing.statistics.statistics import Statistics


class LinReg(Models, ABC):
    def __init__(self, position):
        Models.__init__(self)
        self.position = position

    def run(self):
        # load stats for position
        df = pd.DataFrame()
        for year in range(2016, 2022):
            df = pd.concat([df, Statistics(self.position, year, refresh=True).get_accumulated_data()])
        df.to_csv("test.csv")


if __name__ == "__main__":
    LinReg("QB").run()


