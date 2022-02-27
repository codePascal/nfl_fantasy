"""
Implements the data loading from various websites. If the data is not
available offline, it is freshly fetched from corresponding website.
"""
import os
import pandas as pd


class Loader:
    def __init__(self, refresh=False):
        # path to store data
        self.filename = str()
        self.dir = str()

        # url to fetch data from
        self.url = str()

        # original columns to restore data back to original
        self.original_columns = list()

        # boolean denoting to refresh stored data
        self.refresh = refresh

        # column names and type mapping
        self.mapping = dict()

        # data to add as columns to dataframe
        self.to_add = dict()

    def clean_data(self, df):
        """ Cleans the data by mapping new column names and
        adding defined columns to data. """
        # map column names
        df = self.map_columns(df)

        # fix a thousand notations
        for column in df.columns.to_list():
            df[column] = df[column].apply(self.fix_thousands)

        # add specified data to dataframe
        for key, val in self.to_add.items():
            df[key] = val

        return df.astype(self.mapping)

    def fetch_data(self):
        """ Returns fetched data from URL. """
        return self.get_html_content()

    def get_data(self):
        """ Returns data by fetching, refreshing or only loading. """
        if not os.path.exists(os.path.join(self.dir, self.filename)):
            self.refresh = False
            return self.clean_data(self.fetch_data())
        elif self.refresh:
            return self.refresh_data()
        else:
            return self.load_data()

    def get_html_content(self):
        """ Transforms URL content to table. """
        raise NotImplementedError

    def get_mapping(self):
        """ Returns mapping for original columns. """
        return self.mapping

    @staticmethod
    def get_row_data(tr, tag='td'):
        """ Extracts data from row and creates list.

        :param tr: row in table
        :type tr: tag
        :param tag: tag to find in row
        :type tag: tag
        :return: row as list
        :rtype: list
        """
        return [td.get_text(strip=True) for td in tr.find_all(tag)]

    def get_table_data(self, table):
        """ Extracts data from table and creates list of lists.

        :param table: data in HTML content
        :type table: HTML content
        :return: data parsed to list
        :rtype: list of lists
        """
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

    def load_data(self):
        """ Loads data from file path. """
        return pd.read_csv(os.path.join(self.dir, self.filename))

    def map_columns(self, df):
        """ Maps descriptive column names. """
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = list(self.mapping.keys())
        return df

    def refresh_data(self):
        """ Refreshes stored data by cleaning the data again. """
        return self.clean_data(self.restore_data(self.load_data()))

    def restore_data(self, df):
        """ Restores dataframe back to original columns and column
        names. """
        df = df.iloc[:, :len(self.original_columns)]
        df.columns = self.original_columns
        return df

    def store_data(self):
        """ Stores fetched or refreshed data. """
        if not os.path.exists(self.dir):
            os.makedirs(os.path.join(os.getcwd(), self.dir))
        self.get_data().to_csv(os.path.join(self.dir, self.filename), index=False)

    @staticmethod
    def fix_thousands(number):
        """ Removes trailing comma in integer number. """
        if "," in str(number):
            return int(str(number).replace(",", ""))
        else:
            return number
