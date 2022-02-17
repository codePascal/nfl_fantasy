"""
Gets tables presented by https://www.fantasypros.com/nfl/ and stores
them as .csv files.
"""
import bs4
import pandas as pd
import requests


def get_html_content(url):
    # get HTML config
    req = requests.get(url)

    # observe HTML output -> https://webformatter.com/html
    # print(req.text)

    # get table data
    soup = bs4.BeautifulSoup(req.content, "html.parser")
    table = soup.find(id="data")
    data = get_table_data(table)

    # return as pandas DataFrame
    return pd.DataFrame(data[1:], columns=data[0])


def get_row_data(tr, tag='td'):
    return [td.get_text(strip=True) for td in tr.find_all(tag)]


def get_table_data(table):
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


def get_url_snapcounts(year, week=None):
    if week is None:
        return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={year}&snaps=0&range=full"
    return f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={week}&snaps=0&range=week&year={year}"


def get_url_stats(year, position, week=None):
    if week is None:
        return f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}&range=full"
    return f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}&week={week}&range=week"
