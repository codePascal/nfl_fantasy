"""
Implements the data loading for points allowed.

Fantasy Points Allowed is a metric that indicates how good or bad
each NFL defense is at limiting fantasy production to their
opponents. Teams that rank in the top 8 surrender the most fantasy
points. They represent easy matchups that fantasy owners should
target. On the flip side, teams that rank in the bottom 8 are
difficult matchups that fantasy owners should take into
consideration for start/sit decisions.

Most recent years (back to 2015) are available. However, in some
cases, e.g. Las Vegas Raiders, the name of the team has changed.
Since team names are kept up to date, the points allowed for such a
team are not available. Further, the points of the previous name are
not available too.

If this script is run, all points allowed for denoted year range are
stored.
"""
import bs4
import pandas as pd
import requests

from abc import ABC

from config.fantasypros import pa_type
from config.mapping import team_map
from src.loader.fantasypros.fantasypros import FantasyProsLoader as Loader

# TODO find other source, recent years are not complete


class PointsAllowed(Loader, ABC):
    def __init__(self, year, refresh=False):
        Loader.__init__(self, year, refresh)
        self.mapping = pa_type
        self.to_add = {"year": self.year}

        self.filename = f"points_allowed_{self.year}.csv"
        self.dir = f"../raw/points_allowed"
        self.url = f"https://www.fantasypros.com/nfl/points-allowed.php?year={self.year}"

        # TODO add restoring
        self.refresh = False

    def clean_data(self, df):
        """ Cleans data specifically for points allowed. """
        df = self.map_columns(df)

        # assign team shortcut
        df["team"] = df["team"].apply(add_team_shortcut)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        # set column types
        return df.astype(self.mapping)

    def get_html_content(self):
        """ Reads HTML content and returns data table. """
        # get HTML config
        print("Fetching from", self.url)
        req = requests.get(self.url)

        # observe HTML output -> https://webformatter.com/html
        # print(req.text)

        # get table raw
        soup = bs4.BeautifulSoup(req.content, "html.parser")
        table = soup.find(id="data")
        data = self.get_table_data(table)

        # in that specific case, the content of the table is within one single list
        data_mod = list()
        data_mod.append(data[0])
        for i in range(0, len(data[1]), 13):
            data_mod.append(data[1][i:i+13])

        # return as pandas DataFrame
        return pd.DataFrame(data_mod[1:], columns=data[0])


def add_team_shortcut(team):
    """ Replaces team name with commonly used shortcut. """
    return team_map[team]


def store_all():
    """ Stores all points allowed for given year range. """
    years = (2016, 2021)
    for year in range(years[0], years[1] + 1):
        PointsAllowed(year).store_data()


if __name__ == "__main__":
    store_all()
