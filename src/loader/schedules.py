import pandas as pd
import os

import src.utils.cleaner as cleaner
import src.utils.io as io

from src.config.mapping import week_map


# TODO check where storage location for package would be
PREFIX = "../raw"


def update():
    for year in week_map.keys():
        get_schedule(year)


def get_schedule(year):
    path = f"{PREFIX}/schedules/schedule_{year}.csv"

    if not os.path.exists(path):
        url = f"https://www.fantasypros.com/nfl/schedule/grid.php?year={year}"
        data = io.get_from_fantasypros(url)
        df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df.columns = ["team"] + ["week_" + str(i) for i in range(1, df.shape[1])]
    df.set_index("team", drop=True, inplace=True)

    schedule = pd.DataFrame(columns=["team", "opponent", "week", "home"])
    for i, games in df.iterrows():
        for j, game in enumerate(games):
            schedule = pd.concat([schedule, pd.DataFrame({"team": [i],
                                                          "opponent": [cleaner.get_opponent(game)],
                                                          "week": [j + 1],
                                                          "home": [cleaner.get_location(game)]})],
                                 ignore_index=True)

    schedule["year"] = year

    return schedule

