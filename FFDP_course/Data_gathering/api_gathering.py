"""
Example script to gather data from an API.

Source:
   https://www.fantasyfootballdatapros.com/course/section/13
"""
import requests


def get_fantasy_points(player, pos):
    if player.get("position") == pos:
        return player.get("fantasy_points").get("ppr")


pos = "WR"
year = "2019"
week = 1

req = requests.get('https://www.fantasyfootballdatapros.com/api/players/{0}/{1}'.format(year, week))

if req.ok:
    print("Season {0}, week {1} VOR for {2}s".format(year, week, pos))
    print("-*" * 40)

    data = req.json()
    wr_points = [get_fantasy_points(player, pos) for player in data]
    wr_points = list(filter(lambda x: x is not None, wr_points))

    mean = lambda x: sum(x) / len(x)
    wr_points_mean = mean(wr_points)

    for player in data:
        if player.get("position") == pos:
            vor = player.get("fantasy_points").get("ppr") - wr_points_mean
            print(player.get("player_name"), "had a VOR of", vor)
