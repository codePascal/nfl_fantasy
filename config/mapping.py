""" Holds general definitions for the whole project. """

# maps number of weeks per season
week_map = {
    2021: 18,
    2020: 17,
    2019: 17,
    2018: 17,
    2017: 17,
    2016: 17,
    2015: 17,
    2014: 17,
    2013: 17,
    2012: 17,
    2011: 17,
    2010: 17,
    2009: 17,
}

# maps the current team names to commonly used abbreviations
team_map = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAC",
    "Kansas City Chiefs": "KC",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Las Vegas Raiders": "LV",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}

# stores list of team abbreviations
teams = list(team_map.values())

# map team changes: https://de.wikipedia.org/wiki/National_Football_League#Mannschaften
team_changes_map = {
    "JAX": "JAC",
    "GNB": "GB",
    "NWE": "NE",
    "SFO": "SF",
    "NOR": "NO",
    "KAN": "KC",
    "TAM": "TB",
    "2TM": "CIN",  # TODO verify
    "HTX": "HOU",
    "CLT": "IND",
    "RAV": "BAL",
    "CRD": "ARI",
    "OTI": "TEN",
    "RAI": "LV",  # changed team name in 2020
    "OAK": "LV",  # changed team name in 2020
    "SD": "LAC",  # changed team name in 2017
    "SDG": "LAC",  # changed team name in 2017
    "STL": "LAR",  # changed team name in 2016
    "RAM": "LAR",  # changed team name in 2016
}
