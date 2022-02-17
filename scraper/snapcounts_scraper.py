"""
Gets NFL snap-count analysis from website
https://www.fantasypros.com/nfl/reports/snap-count-analysis/.
"""
import argparse
import os

import scraper as scp


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("--week", type=int)
    args = parser.parse_args()

    # get table
    df = scp.get_html_content(scp.get_url_snapcounts(args.year, args.week))

    # store raw
    if args.week is not None:
        if not os.path.exists(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{args.year}")):
            os.makedirs(os.path.join(os.getcwd(), f"../raw/weekly_snapcounts/{args.year}"))
        df.to_csv(f"../raw/weekly_snapcounts/{args.year}/week_{args.week}.csv")
    else:
        if not os.path.exists(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts")):
            os.makedirs(os.path.join(os.getcwd(), f"../raw/yearly_snapcounts"))
        df.to_csv(f"../raw/yearly_snapcounts/snapcounts_{args.year}.csv")
