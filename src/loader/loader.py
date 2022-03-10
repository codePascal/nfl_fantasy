"""
Implements the data loading from various websites. If the data is not
available offline, it is freshly fetched from corresponding website,
stored and returned. Otherwise, the data is just loaded and returned.
"""
import os
import pandas
import pandas as pd
import requests
import bs4


class Loader:
    def __init__(self):
        self.dir = str()
        self.filename = str()
        self.mapping = dict()
        self.to_add = dict()
        self.url = str()

    def add_columns(self, df):
        for key, val in self.to_add.items():
            df[key] = val
        return df

    def assign_type(self, df):
        return df.astype(self.mapping)

    def check_columns(self, df):
        for column in df.columns.to_list():
            df[column] = df[column].apply(self.fix_thousands)
        return df

    def clean_data(self, df):
        df = self.map_columns(df)
        df = self.add_columns(df)
        df = self.fix_columns(df)
        df = self.check_columns(df)
        df = self.assign_type(df)
        return df

    def fetch_data(self):
        return self.get_html_content()

    def fix_columns(self, df):
        return df

    @staticmethod
    def fix_thousands(number):
        if "," in str(number):
            return int(str(number).replace(",", ""))
        else:
            return number

    def get_data(self):
        if not os.path.exists(os.path.join(self.dir, self.filename)):
            self.store_data()
        return self.clean_data(self.load_data())

    def get_html_content(self):
        data = self.get_table_data(self.get_table(self.get_soup(self.get_request())))
        return self.transform_to_frame(data)

    def get_request(self):
        print("Fetching from", self.url)
        return requests.get(self.url)

    @staticmethod
    def get_row_data(tr, tag='td'):
        return [td.get_text(strip=True) for td in tr.find_all(tag)]

    @staticmethod
    def get_soup(request):
        return bs4.BeautifulSoup(request.content, "html.parser")

    @staticmethod
    def get_table(soup):
        return soup.find(id="data")

    def get_table_data(self, table):
        rows = table.find_all('tr')
        data = list()
        header_row = 0
        for i, row in enumerate(rows):
            if self.get_row_data(row, 'th'):
                data.append(self.get_row_data(row, 'th'))
                header_row = i
        for row in rows[header_row + 1:]:
            data.append(self.get_row_data(row))
        return data

    def map_columns(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = list(self.mapping.keys())
        return df

    def load_data(self):
        return pd.read_csv(os.path.join(self.dir, self.filename))

    @staticmethod
    def transform_to_frame(data):
        return pd.DataFrame(data[1:], columns=data[0])

    def store_data(self):
        if not os.path.exists(self.dir):
            os.makedirs(os.path.join(os.getcwd(), self.dir))
        self.fetch_data().to_csv(os.path.join(self.dir, self.filename), index=False)

