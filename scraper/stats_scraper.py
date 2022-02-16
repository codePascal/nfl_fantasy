"""
Gets NFL stats from website https://www.fantasypros.com/nfl/stats/.
"""
import argparse
import os

import scraper as scp


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("position", type=str)
    parser.add_argument("--week", type=int)
    args = parser.parse_args()

    # get table
    df = scp.get_html_content(scp.get_url_stats(args.year, args.position, args.week))

    # store data
    if args.week is not None:
        if not os.path.exists(os.path.join(os.getcwd(), f"../data/weekly_stats/{args.year}/{args.position.upper()}")):
            os.makedirs(os.path.join(os.getcwd(), f"../data/weekly_stats/{args.year}/{args.position.upper()}"))
        df.to_csv(f"../data/weekly_stats/{args.year}/{args.position.upper()}/week_{args.week}.csv")
    else:
        if not os.path.exists(os.path.join(os.getcwd(), f"../data/yearly_stats/{args.position.upper()}")):
            os.makedirs(os.path.join(os.getcwd(), f"../data/yearly_stats/{args.position.upper()}"))
        df.to_csv(f"../data/yearly_stats/{args.position.upper()}/{args.position.upper()}_{args.year}.csv")
