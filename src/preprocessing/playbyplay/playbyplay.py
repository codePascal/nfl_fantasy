import os
import gzip
import shutil
import pandas as pd
import tqdm


def extract_file(year):
    """
    Extract and stores play-by-play data for a given year.

    :param year: year to evaluate
    :type year: int
    :return: None
    """
    with gzip.open(f"../../nflfastR-data/data/play_by_play_{year}.csv.gz", 'rb') as f_in:
        with open(f"../raw/play-by-play/play_by_play_{year}.csv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_playbyplay_data(year):
    """
    Returns the play-by-play data for a given year.

    :param year: year to evaluate
    :type year: int
    :return: Play-by-play data with year added
    :rtype: pandas.DataFrame
    """
    # check if file exists
    if not os.path.exists(f"../raw/play-by-play/play_by_play_{year}.csv"):
        extract_file(year)

    # read in chunks and store as dataframe
    df = pd.DataFrame()
    chunks = pd.read_csv(f"../raw/play-by-play/play_by_play_{year}.csv", iterator=True, low_memory=False,
                         chunksize=10000)
    for chunk in chunks:
        chunk["year"] = year
        df = pd.concat([df, chunk])
    return df


def concat_playbyplay_data(years):
    """
    Returns the play-by-play data for a given year range.

    :param years: year range
    :type years: tuple
    :return: Play-by-play data for the given range
    :rtype: pandas.DataFrame
    """
    df_accumulated = pd.DataFrame()
    for year in tqdm.tqdm(range(years[0], years[1] + 1)):
        df_accumulated = pd.concat([df_accumulated, get_playbyplay_data(year)])
    return df_accumulated


if __name__ == "__main__":
    years = (1999, 2021)
    # TODO write in chunks
    concat_playbyplay_data(years).to_csv(f"../preprocessed/play-by-play/pbp_{years[0]}to{years[1]}.csv", index=False)
