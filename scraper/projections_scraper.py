"""
Gets recent NFL projections from website
https://www.fantasypros.com/nfl/projections/.
"""
import argparse
import os

import scraper as scp


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("position", type=str)
    parser.add_argument("week", type=int)
    args = parser.parse_args()

    # get table
    df = scp.get_html_content(scp.get_url_projections(args.position, args.week))

    # store raw
    if not os.path.exists(os.path.join(os.getcwd(), f"../raw/projections/{args.position.upper()}")):
        os.makedirs(os.path.join(os.getcwd(), f"../raw/projections/{args.position.upper()}"))
    df.to_csv(f"../raw/projections/{args.position.upper()}/week_{args.week}.csv")
