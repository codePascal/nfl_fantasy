"""
Implements the data fetching from https://www.fantasypros.com/nfl.
Various data is available, the tables are represented with id=data.
"""
import bs4
import pandas as pd
import requests


def get_html_content(url):
    """
    Reads the HTML content and creates table from given id=data.

    :param url: URL to read content
    :type url: str
    :return: table stored in content
    :rtype: pandas.DataFrame
    """
    # get HTML config
    print("Fetching from", url)
    req = requests.get(url)

    # observe HTML output -> https://webformatter.com/html
    # print(req.text)

    # get table raw
    soup = bs4.BeautifulSoup(req.content, "html.parser")
    table = soup.find(id="data")
    data = get_table_data(table)

    # return as pandas DataFrame
    return pd.DataFrame(data[1:], columns=data[0])


def get_row_data(tr, tag='td'):
    """
    Extracts data from row and creates list.

    :param tr: row in table
    :type tr: tag
    :param tag: tag to find in row
    :type tag: tag
    :return: row as list
    :rtype: list
    """
    return [td.get_text(strip=True) for td in tr.find_all(tag)]


def get_table_data(table):
    """
    Extracts data from table and creates list of lists.

    :param table: data in HTML content
    :type table: HTML content
    :return: data parsed to list
    :rtype: list of lists
    """
    rows = table.find_all('tr')
    data = list()
    header_row = 0
    for i, row in enumerate(rows):
        if get_row_data(row, 'th'):
            data.append(get_row_data(row, 'th'))
            header_row = i
    for row in rows[header_row + 1:]:
        data.append(get_row_data(row))

    return data
