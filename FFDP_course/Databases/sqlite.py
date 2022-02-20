"""
Example script to handle databases with sqlite.

Source:
    https://www.fantasyfootballdatapros.com/course/section/15
"""
import sqlite3
import pandas as pd
import requests
from collections import OrderedDict


def transform_json(player):
    data = dict()

    # add outer stats
    for k, v in player.items():
        if k != "stats":
            # replace apostrophes in name
            if k == "player_name":
                v = v.replace("'", "")
            data[k] = v

    # remove nesting
    sub_stats = [player["stats"]["rushing"], player["stats"]["passing"], player["stats"]["receiving"]]
    for sub_stat in sub_stats:
        for k, v in sub_stat.items():
            data[k] = v

    return sorted(data.items())


if __name__ == "__main__":
    # instantiate database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # define columns for table
    columns = [('player_name', 'text'), ('int', 'real'), ('fumbles_lost', 'real'), ('games_played', 'real'),
               ('position', 'text'), ('passing_att', 'real'), ('passing_cmp', 'real'), ('passing_td', 'real'),
               ('passing_yds', 'real'), ('receiving_yds', 'real'), ('receiving_td', 'real'), ('receptions', 'real'),
               ('targets', 'real'), ('rushing_td', 'real'), ('rushing_att', 'real'), ('rushing_yds', 'real'),
               ('team', 'text')]

    # sort regarding column name
    columns = sorted(columns, key=lambda x: x[0])

    # command to create table
    create_table_cmd = "CREATE TABLE stats2019"
    for index, (col, type) in enumerate(columns):
        if index == 0:
            create_table_cmd += " ({} {}".format(col, type)
        elif index != 0 and index != len(columns) - 1:
            create_table_cmd += ", {} {}".format(col, type)
        else:
            create_table_cmd += ", {} {})".format(col, type)

    # create table
    cursor.execute(create_table_cmd)
    conn.commit()

    # fetch 2019 stats
    req = requests.get('https://www.fantasyfootballdatapros.com/api/players/2019/all')
    json = req.json()

    # get a one dimensional dict for each player
    json_mod = list(map(transform_json, json))

    # create insert command for each player
    insert_cmd = list()
    for player in json_mod:
        cmd = "INSERT INTO stats2019 VALUES("
        for index, (_, stat) in enumerate(player):
            if index == len(player) - 1:
                cmd += " '{}')".format(stat)
            else:
                cmd += "'{}', ".format(stat)
        insert_cmd.append(cmd)

    # insert each player to table
    for cmd in insert_cmd:
        cursor.execute(cmd)
        conn.commit()

    # select command
    select_all_cmd = "SELECT * FROM stats2019"
    cursor.execute(select_all_cmd)
    out = cursor.fetchall()
    print(out[0])

    # print top 10 receiving TD players
    i = 1
    for row in cursor.execute("SELECT * FROM stats2019 ORDER BY receiving_td DESC"):
        if i < 10:
            print(row)
        i += 1

