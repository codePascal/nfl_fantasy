"""
Gets NFL snap-count analysis from website
https://www.fantasypros.com/nfl/reports/snap-count-analysis/.
"""

import argparse
import bs4
import pandas as pd
import requests


def get_row_data(tr, tag='td'):
    return [td.get_text(strip=True) for td in tr.find_all(tag)]


def get_table_data(table):
    # parse all rows to a list
    rows = table.find_all('tr')

    # get data
    data = list()
    header_row = 0
    for i, row in enumerate(rows):
        if get_row_data(row, 'th'):
            data.append(get_row_data(row, 'th'))
            header_row = i
    for row in rows[header_row + 1:]:
        data.append(get_row_data(row))

    return data


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("week", type=int)
    args = parser.parse_args()

    # check if page can be scraped with "url/robots.txt"
    URL =f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={args.week}&snaps=0&range=week&year={args.year}"

    # get HTML config
    req = requests.get(URL)

    # observe HTML output -> https://webformatter.com/html
    # print(req.text)

    # get table data
    soup = bs4.BeautifulSoup(req.content, "html.parser")
    table = soup.find(id="data")
    data = get_table_data(table)

    # store table as pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(f"../data/snapcounts/{args.year}/week_{args.week}.csv")
