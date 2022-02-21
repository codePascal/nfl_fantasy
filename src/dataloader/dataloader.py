"""
Fetches tables presented by https://www.fantasypros.com/nfl/ and
stores them as .csv files.
"""
import bs4
import os
import pandas as pd
import requests


def fetch_projections(position, week):
    """
    Fetches and stores latest projections for next year from
    https://www.fantasypros.com/nfl/projections/.

    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/projections/{position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/projections/{position.upper()}"))
    get_html_content(get_url_projections(position, week)).to_csv(
        f"../raw/projections/{position.upper()}/week_{week}.csv")


def fetch_schedule(year):
    """
    Fetches and stores schedule from
    https://www.fantasypros.com/nfl/schedule/grid.php.

    :param year: year to fetch
    :type year: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/schedules")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/schedules"))
    get_html_content(get_url_schedule(year)).to_csv(f"../raw/schedules/schedule_{year}.csv")


def fetch_snapcounts_weekly(year, week):
    """
    Fetches and stores the weekly snapcounts from
    https://www.fantasypros.com/nfl/reports/snap-count-analysis/.

    :param year: year to fetch
    :type year: int
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{year}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{year}"))
    get_html_content(get_url_snapcounts_weekly(year, week)).to_csv(
        f"../raw/weekly_snapcounts/{year}/week_{week}.csv")


def fetch_snapcounts_yearly(year):
    """
    Fetches and stores the yearly snapcounts from
    https://www.fantasypros.com/nfl/reports/snap-count-analysis/.

    :param year: year to fetch
    :type year: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts"))
    get_html_content(get_url_snapcounts_yearly(year)).to_csv(
        f"../raw/yearly_snapcounts/snapcounts_{year}.csv")


def fetch_stats_weekly(year, position, week):
    """
    Fetches and stores weekly stats from
    https://www.fantasypros.com/nfl/stats/.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :param week: week to fetch
    :type week: int
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/weekly_stats/{year}/{position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/weekly_stats/{year}/{position.upper()}"))
    get_html_content(get_url_stats_weekly(year, position, week)).to_csv(
        f"../raw/weekly_stats/{year}/{position.upper()}/week_{week}.csv")


def fetch_stats_yearly(year, position):
    """
    Fetches and stores yearly stats from
    https://www.fantasypros.com/nfl/stats/.

    :param year: year to fetch
    :type year: int
    :param position: position to fetch
    :type position: str
    :return: None
    """
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/yearly_stats/{position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/yearly_stats/{position.upper()}"))
    get_html_content(get_url_stats_yearly(year, position)).to_csv(
        f"../raw/yearly_stats/{position.upper()}/{position.upper()}_{year}.csv")


def get_html_content(url):
    """
    Reads the HTML content and creates table from given id=data.

    :param url: URL to read content
    :type url: str
    :return: table stored in content
    :rtype: pandas.DataFrame
    """
    # get HTML config
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


def get_url_projections(position, week):
    return f"https://www.fantasypros.com/nfl/projections/{position}.php?week={week}"


def get_url_schedule(year):
    return f"https://www.fantasypros.com/nfl/schedule/grid.php?year={year}"


def get_url_snapcounts_weekly(year, week):
    return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={week}&snaps=0&range=week&year={year}"


def get_url_snapcounts_yearly(year):
    return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={year}&snaps=0&range=full"


def get_url_stats_weekly(year, position, week):
    return f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}&week={week}&range=week"


def get_url_stats_yearly(year, position):
    return f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}&range=full"


if __name__ == "__main__":
    year = 2015
    position = "QB"
    week = 1
    fetch_stats_weekly(year, position, week)
