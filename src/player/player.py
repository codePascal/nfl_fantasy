from .. util.connection import Connection


class Player:
    def __init__(self, name, connection):
        # open connection to database
        self.connection = connection

        # the players name
        self.name = name

    def get_name(self):
        return self.name

    def get_team(self, year):
        return self.connection.query_database_cell(
            "select Tm from `{}_yearly` where Player='{}'".format(year, self.name)
        )

    def get_position(self):
        return self.connection.query_database_cell(
            "select Pos from `2019_yearly` where Player='{}'".format(self.name)
        )

    def get_age(self, year):
        return self.connection.query_database_cell(
            "select Age from `{}_yearly` where Player='{}'".format(year, self.name)
        )

    def get_fumbles(self, year):
        return self.connection.query_database_cell(
            "select Fumbles from `{}_yearly` where Player='{}'".format(year, self.name)
        )

    def get_fumbles_lost(self, year):
        return self.connection.query_database_cell(
            "select FumblesLost from `{}_yearly` where Player='{}'".format(year, self.name)
        )

    def get_yearly_points(self, year):
        return self.connection.query_database_cell(
            "select FantasyPoints from `{}_yearly` where Player='{}'".format(year, self.name)
        )

    def get_weekly_points(self, year, week):
        return self.connection.query_database_cell(
            "select StandardFantasyPoints from `{}_weekly_week{}` where Player='{}'".format(year, week, self.name)
        )

    def wrap_yearly_points(self):
        points = list()
        for year in self.connection.available_years:
            points.append(self.get_yearly_points(year))
        return points

    def wrap_weekly_points(self, year):
        points = list()
        for week in range(1, 18):
            points.append(self.get_weekly_points(year, week))
        return points
