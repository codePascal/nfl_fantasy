"""
Gets NFL schedules from website
https://www.fantasypros.com/nfl/schedule/grid.php.
"""
import argparse
import os

import scraper as scp


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    args = parser.parse_args()

    # get table
    df = scp.get_html_content(scp.get_url_schedule(args.year))

    # store raw
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/schedules")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/schedules"))
    df.to_csv(f"../raw/schedules/schedule_{args.year}.csv")
