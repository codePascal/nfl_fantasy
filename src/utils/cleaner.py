import numpy as np

import src.config.mapping as mapping


def add_columns(df, data):
    for key, val in data.items():
        df[key] = val
    return df


def assign_type(df, types):
    return df.astype(types)


def check_columns(df):
    for column in df.columns.to_list():
        df[column] = df[column].apply(fix_thousands)
    return df


def fix_thousands(number):
    if "," in str(number):
        return int(str(number).replace(",", ""))
    else:
        return number


def drop_unnamed(df):
    return df.loc[:, ~df.columns.str.contains("^Unnamed")]


def map_column_names(df, mapping):
    df.columns = list(mapping.keys())
    return df


def get_team_stats(player):
    return player.split('(')[1].split(')')[0]


def get_team_projections(player):
    if player in mapping.team_map.keys():
        return mapping.team_map[player]
    else:
        for subname in player.split():
            for team in mapping.teams:
                if team in subname:
                    return team


def add_team_abbreviation(team):
    if team in mapping.teams:
        return team
    elif team in mapping.team_map:
        return mapping.team_map[team]
    elif team in mapping.team_changes_map:
        return mapping.team_changes_map[team]
    else:
        print(team, "not found.")
        return team


def fix_player_stats(player):
    if '(' in player:
        return player.split('(')[0]
    return player


def fix_player_projections(player):
    to_drop = ""
    for subname in player.split():
        for team in mapping.teams:
            if team in subname:
                to_drop = team
    return player.replace(to_drop, "")


def fix_rost(rost):
    if "%" in str(rost):
        return str(rost).replace("%", "")
    return rost


def get_opponent(game):
    if game == "BYE" or game == '-':
        return "BYE"
    elif game.startswith("@"):
        return game[1:]
    elif game.startswith("vs"):
        return game[2:]


def get_location(game):
    if game.startswith('@'):
        return False
    elif game.startswith("vs"):
        return True
    else:
        return np.nan
