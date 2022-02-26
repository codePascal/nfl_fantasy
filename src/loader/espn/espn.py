"""
...
"""
import bs4
import itertools
import pandas as pd
import requests

from abc import ABC

from src.loader.loader import Loader


class EspnLoader(Loader, ABC):
    def __init__(self, year, season, refresh=False):
        Loader.__init__(self, refresh)
        self.year = year
        self.season = season
        self.seasontype = get_season_type(self.season)
        self.skip = 0

    def get_html_content(self):
        """ Reads HTML content and returns data table. """
        # get HTML config
        print("Fetching from", self.url)
        req = requests.get(self.url)

        # observe HTML output -> https://webformatter.com/html
        # print(req.text)

        # get table raw
        soup = bs4.BeautifulSoup(req.content, "html.parser")
        tables = soup.find(class_="ResponsiveTable").find_all("table")
        idx = list(itertools.chain.from_iterable(self.get_table_data(tables[0])))
        content = self.get_table_data(tables[1])

        # in case table has two headers:
        if self.skip > 0:
            idx = idx[self.skip:]
            content = content[self.skip:]

        # parse to table
        data = pd.DataFrame(content[1:], index=idx[1:], columns=content[0])
        data.index = data.index.set_names([idx[0]])
        data.reset_index(inplace=True)

        return data


def get_season_type(season):
    if season == "PRE":
        return 1
    elif season == "REG":
        return 2
    elif season == "POST":
        return 3


if __name__ == "__main__":
    pass
