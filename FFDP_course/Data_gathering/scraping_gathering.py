"""
Example script to gather data via web scraping.

Source:
    https://www.fantasyfootballdatapros.com/course/section/14
"""
import pandas as pd
import requests

from bs4 import BeautifulSoup as BS

URL = 'https://www.fantasyfootballdatapros.com/table'

req = requests.get(URL)

if req.ok:
    print('Response was OK!')

    soup = BS(req.content, "html.parser")
    table = soup.find("table")

    df = pd.read_html(str(table))[0]
    df = df.iloc[:, 1:]
    print(df)
