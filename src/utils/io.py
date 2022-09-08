import os
import pandas as pd
import gzip
import shutil

import src.utils.parser as parser


def extract_data(url, path):
    with gzip.open(url, 'rb') as f_in:
        with open(path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_from_espn(url):
    identifier = ("table", {"class": "Table"})
    return parser.fetch(url, identifier)


def get_from_fantasypros(url):
    identifier = ("table", {"class": "table"})
    return parser.fetch(url, identifier)


def load_data(path):
    df = pd.DataFrame()
    chunks = pd.read_csv(path, iterator=True, low_memory=False, chunksize=10000)
    for chunk in chunks:
        df = pd.concat([df, chunk])
    return df


def store(path, df):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.join(os.getcwd(), os.path.dirname(path)))
    df.to_csv(path, index=False)

