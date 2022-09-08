import itertools
import pandas as pd
import os

import src.utils.cleaner as cleaner
import src.utils.io as io

import src.config.fantasypros as fp_mapping
import src.config.espn as espn_mapping
from src.config.mapping import week_map


PREFIX = "../raw"


def get_accumulated_weekly_stats(position, year):
    df = pd.DataFrame()
    for week in range(1, week_map[year] + 1):
        weekly = get_weekly_stats(position, week, year)
        df = pd.concat([df, weekly])
    return df


def get_accumulated_weekly_snapcounts(year):
    df = pd.DataFrame()
    for week in range(1, week_map[year] + 1):
        weekly = get_weekly_snapcounts(week, year)
        df = pd.concat([df, weekly])
    return df


def get_accumulated_projections(position, year=2021):
    df = pd.DataFrame()
    for week in range(1, week_map[year] + 1):
        weekly = get_projections(position, week, year)
        df = pd.concat([df, weekly])
    return df


def get_accumulated_yearly_stats(position):
    df = pd.DataFrame()
    for year in week_map.keys():
        yearly = get_yearly_stats(position, year)
        df = pd.concat([df, yearly])
    return df


def get_accumulated_yearly_snapcounts():
    df = pd.DataFrame()
    for year in week_map.keys():
        yearly = get_yearly_snapcounts(year)
        df = pd.concat([df, yearly])
    return df


def get_offense_stats(year, season="REG"):
    how_ = "inner"
    on_ = ["team", "games_offense", "year"]

    df = get_offense_passing_stats(year, season)
    df = pd.merge(df, get_offense_rushing_stats(year, season), how=how_, on=on_)
    df = pd.merge(df, get_offense_receiving_stats(year, season), how=how_, on=on_)
    return pd.merge(df, get_offense_downs_stats(year, season), how=how_, on=on_)


def get_defense_stats(year, season="REG"):
    how_ = "inner"
    on_ = ["team", "games_defense", "year"]

    df = get_defense_passing_stats(year, season)
    df = pd.merge(df, get_defense_rushing_stats(year, season), how=how_, on=on_)
    df = pd.merge(df, get_defense_receiving_stats(year, season), how=how_, on=on_)
    return pd.merge(df, get_defense_downs_stats(year, season), how=how_, on=on_)


def update():
    for position in ["QB", "RB", "TE", "WR"]:
        for year in week_map.keys():
            get_yearly_stats(position, year)
            for week in range(1, week_map[year] + 1):
                get_weekly_stats(position, week, year)

    for position in ["QB", "RB", "TE", "WR"]:
        for week in range(1, week_map[2021] + 1):
            get_projections(position, week)

    for year in range(2016, list(week_map.keys())[0] + 1):
        get_yearly_snapcounts(year)
        for week in range(1, week_map[year] + 1):
            get_weekly_snapcounts(week, year)

    for year in week_map.keys():
        get_points_allowed(year)

    for year in week_map.keys():
        get_offense_passing_stats(year)
        get_offense_rushing_stats(year)
        get_offense_receiving_stats(year)
        get_offense_downs_stats(year)
        get_defense_passing_stats(year)
        get_defense_rushing_stats(year)
        get_defense_receiving_stats(year)
        get_defense_downs_stats(year)


def get_weekly_stats(position, week, year):
    path = f"{PREFIX}/weekly_stats/{year}/{position.upper()}/week_{week}.csv"

    if not os.path.exists(path):
        url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&week={week}&range=week"
        data = io.get_from_fantasypros(url)
        df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, fp_mapping.stats_type[position])
    df = cleaner.check_columns(df)

    # TODO fix team assignment
    df["team"] = df["player"].apply(cleaner.get_team_stats)

    df["player"] = df["player"].apply(cleaner.fix_player_stats)
    df["rost"] = df["rost"].apply(cleaner.fix_rost)

    df = cleaner.assign_type(df, fp_mapping.stats_type[position])

    df = df.loc[df["games"] == 1]
    df.drop(["rank", "rost", "fantasy_points_per_game"], axis=1, inplace=True)

    df["position"] = position
    df["week"] = week
    df["year"] = year

    return df


def get_yearly_stats(position, year):
    path = f"{PREFIX}/yearly_stats/{year}/{position.upper()}_{year}.csv"

    if not os.path.exists(path):
        url = f"https://www.fantasypros.com/nfl/stats/{position.lower()}.php?year={year}&range=full"
        data = io.get_from_fantasypros(url)
        df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, fp_mapping.stats_type[position])
    df = cleaner.check_columns(df)

    # TODO fix team assignment
    df["team"] = df["player"].apply(cleaner.get_team_stats)

    df["player"] = df["player"].apply(cleaner.fix_player_stats)
    df["rost"] = df["rost"].apply(cleaner.fix_rost)

    df = cleaner.assign_type(df, fp_mapping.stats_type[position])

    df = df.loc[df["games"] >= 1]
    df.drop(["rank", "rost"], axis=1, inplace=True)

    df["position"] = position
    df["year"] = year

    return df


def get_weekly_snapcounts(week, year):
    if year < 2016:
        return None
    else:
        path = f"{PREFIX}/weekly_snapcounts/{year}/week_{week}.csv"

        if not os.path.exists(path):
            url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?week={week}&snaps=0&range=week&year={year}"
            data = io.get_from_fantasypros(url)
            df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
            io.store(path, df)
        else:
            df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, fp_mapping.snapcounts_type)
    df = cleaner.check_columns(df)
    df = cleaner.assign_type(df, fp_mapping.snapcounts_type)

    df = df.loc[df["games"] == 1]
    df.drop(["snaps_per_game"], axis=1, inplace=True)

    df["week"] = week
    df["year"] = year

    return df


def get_yearly_snapcounts(year):
    if year < 2016:
        return None
    else:
        path = f"{PREFIX}/yearly_snapcounts/snapcounts_{year}.csv"

        if not os.path.exists(path):
            url = f"https://www.fantasypros.com/nfl/reports/snap-count-analysis/?year={year}&snaps=0&range=full"
            data = io.get_from_fantasypros(url)
            df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
            io.store(path, df)
        else:
            df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, fp_mapping.snapcounts_type)
    df = cleaner.check_columns(df)
    df = cleaner.assign_type(df, fp_mapping.snapcounts_type)

    df = df.loc[df["games"] >= 1]

    df["year"] = year

    return df


def get_projections(position, week, year=2021):
    path = f"{PREFIX}/projections/{year}/{position.upper()}/week_{week}.csv"

    if not os.path.exists(path):
        url = f"https://www.fantasypros.com/nfl/projections/{position.lower()}.php?week={week}"
        data = io.get_from_fantasypros(url)
        df = pd.DataFrame(data=data[0][1:], columns=data[0][0])
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, fp_mapping.projections_type[position])
    df = cleaner.check_columns(df)
    df = cleaner.assign_type(df, fp_mapping.projections_type[position])

    df["team"] = df["player"].apply(cleaner.get_team_projections)
    df["player"] = df["player"].apply(cleaner.fix_player_projections)

    df["position"] = position
    df["week"] = week
    df["year"] = year

    return df


def get_points_allowed(year):
    path = f"{PREFIX}/points_allowed/points_allowed_{year}.csv"

    if not os.path.exists(path):
        url = f"https://www.fantasypros.com/nfl/points-allowed.php?year={year}"
        data = io.get_from_fantasypros(url)
        data_mod = list()
        for i in range(0, len(data[0][1]), len(data[0][0])):
            data_mod.append(data[0][1][i:i + len(data[0][0])])
        df = pd.DataFrame(data=data_mod, columns=data[0][0])
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, dict([item for item in fp_mapping.pa_type.items()][:df.shape[1]]))
    df = cleaner.check_columns(df)
    df = cleaner.assign_type(df, fp_mapping.pa_type)

    df["year"] = year

    return df


def get_offense_stats(year, season="REG"):
    how_ = "inner"
    on_ = ["team", "games_offense", "year"]

    df = get_offense_passing_stats(year, season)
    df = pd.merge(df, get_offense_rushing_stats(year, season), how=how_, on=on_)
    df = pd.merge(df, get_offense_receiving_stats(year, season), how=how_, on=on_)
    return pd.merge(df, get_offense_downs_stats(year, season), how=how_, on=on_)


def get_offense_passing_stats(year, season="REG"):
    return _get_team_stats(year, "offense", "passing", espn_mapping.offense_passing_map, season)


def get_offense_rushing_stats(year, season="REG"):
    return _get_team_stats(year, "offense", "rushing", espn_mapping.offense_rushing_map, season)


def get_offense_receiving_stats(year, season="REG"):
    return _get_team_stats(year, "offense", "receiving", espn_mapping.offense_receiving_map, season)


def get_offense_downs_stats(year, season="REG"):
    return _get_team_stats(year, "offense", "downs", espn_mapping.offense_downs_map, season, skip=1)


def get_defense_passing_stats(year, season="REG"):
    return _get_team_stats(year, "defense", "passing", espn_mapping.defense_passing_map, season)


def get_defense_rushing_stats(year, season="REG"):
    return _get_team_stats(year, "defense", "rushing", espn_mapping.defense_rushing_map, season)


def get_defense_receiving_stats(year, season="REG"):
    return _get_team_stats(year, "defense", "receiving", espn_mapping.defense_receiving_map, season)


def get_defense_downs_stats(year, season="REG"):
    return _get_team_stats(year, "defense", "downs", espn_mapping.defense_downs_map, season, skip=1)


def get_playbyplay_stats(year):
    path = f"{PREFIX}/play-by-play/play_by_play_{year}.csv"

    if not os.path.exists(path):
        url = f"../../nflfastR-data/data/play_by_play_{year}.csv.gz"
        io.extract_data(url, path)

    df = io.load_data(path)

    df["year"] = year

    return df


def _get_team_stats(year, team, stat, col_map, season="REG", skip=0):
    path = f"{PREFIX}/teamstats/{year}/{team}_{stat}_{year}_{season}.csv"
    seasontype = 2  # TODO Fixme to load post season stats

    if not os.path.exists(path):
        url = f"https://www.espn.com/nfl/stats/team/_/view/{team}/stat/{stat}/season/{year}/seasontype/{seasontype}"
        data = io.get_from_espn(url)
        idx = list(itertools.chain.from_iterable(data[0]))[skip:]
        columns = data[1][skip]
        stats = data[1][skip+1:]
        df = pd.DataFrame(data=stats, index=idx[1:], columns=columns)
        df.index.name = idx[0]
        df.reset_index(inplace=True)
        io.store(path, df)
    else:
        df = pd.read_csv(path)

    df = cleaner.drop_unnamed(df)
    df = cleaner.map_column_names(df, col_map)
    df = cleaner.check_columns(df)
    df = cleaner.assign_type(df, col_map)

    df["team"] = df["team"].apply(cleaner.add_team_abbreviation)

    df["year"] = year

    return df

