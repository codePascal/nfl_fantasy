import gzip
import shutil
import pandas as pd

if __name__ == "__main__":
    # year range
    years = (1999, 2021)

    # extract and copy the files
    for year in range(years[0], years[1] + 1):
        with gzip.open(f"../../nflfastR-data/data/play_by_play_{year}.csv.gz", 'rb') as f_in:
            with open(f"../raw/play-by-play/play_by_play_{year}.csv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # concat the files to one
    df_accumulated = pd.DataFrame()
    for year in range(years[0], years[1] + 1):
        # load in single chunks
        chunks = pd.read_csv(f"../raw/play-by-play/play_by_play_{year}.csv", iterator=True, low_memory=False,
                             chunksize=10000)

        # concat to dataframe
        df = pd.DataFrame()
        for chunk in chunks:
            df = pd.concat([df, chunk])
        df["year"] = year

        if year == years[0]:
            df_accumulated = df.copy()
        else:
            df_accumulated = pd.concat([df_accumulated, df], axis=0, ignore_index=True)

    df_accumulated.to_csv(f"../preprocessed/play-by-play/pbp_{years[0]}to{years[1]}.csv", index=False)


