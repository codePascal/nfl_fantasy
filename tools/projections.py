import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import utils.data_handling as dh
import utils.fantasy_pros as fp


if __name__ == "__main__":
    # defines
    player = "Kyler Murray"

    # yearly schedule
    schedule = dh.read_csv_file("../data/schedules/schedule_2021.csv")
    schedule = schedule.dropna()
    schedule = fp.clean_schedule(schedule)

    # accumulate weekly stats
    X_data = pd.DataFrame()
    y_data = pd.Series(dtype=float)
    for week in range(1, 8):
        # get player statistics of defined week
        player_stats = dh.read_csv_file("../data/weekly/2021/QB/week_{}.csv".format(week))
        player_stats = player_stats.dropna()
        player_stats = fp.clean_stats_qb(player_stats)

        # get defined player
        player_stats.set_index("player", drop=True, inplace=True)
        player_stats = player_stats.loc[player]

        # get opponent and location of game
        opp = fp.get_opponent(schedule, player_stats["team"], week)
        home = fp.get_place(schedule, player_stats["team"], week)

        # get stats of defense
        defense_stats = dh.read_csv_file("../data/weekly/2021/DEF/week_{}.csv".format(week))
        defense_stats = defense_stats.dropna()
        defense_stats = fp.clean_stats_def(defense_stats)
        defense_stats.set_index("team", drop=True, inplace=True)
        defense_stats = defense_stats.loc[opp]

        # accumulate stats
        pd.set_option("display.max_columns", None)
        player_stats = player_stats.loc[["passing_cmp", "passing_att", "passing_pct", "passing_yds", "passing_td",
                                         "passing_int", "passing_sacks", "rushing_att", "rushing_yds", "rushing_td",
                                         "misc_fpts"]]
        defense_stats = defense_stats.loc[["defense_sacks", "defense_ints", "fumble_recovery", "fumble_forced",
                                           "defense_td", "defense_safety", "misc_fpts"]]
        home_stats = pd.Series(home, index=["home"])

        X_data["week_{}".format(week)] = pd.concat([player_stats.drop("misc_fpts"), defense_stats, home_stats])
        y_data["week_{}".format(week)] = player_stats.loc["misc_fpts"]

    # linear regression
    X = X_data.values.transpose()
    y = y_data.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(y_pred, y_test)














