from mysql.connector import connect, Error


class Connection:
    def __init__(self):
        self.cnx = self.connect_to_database()
        self.cursor = self.cnx.cursor()
        self.available_years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

    @staticmethod
    def connect_to_database():
        try:
            cnx = connect(
                host="localhost",
                user="pascal",
                password="anno1602",
                database="nfl_fantasy_stats_yearly")
            print("Login to database successful.")
            return cnx
        except Error as e:
            print("Failed to connect to database: {}".format(e))

    def query_database_cell(self, query):
        self.execute_query(query)
        return self.cursor.fetchone()

    def query_database_row(self, query):
        raise NotImplementedError

    def query_database_col(self, query):
        raise NotImplementedError

    def execute_query(self, query):
        print("Executing query: {}".format(query))
        try:
            self.cursor.execute(query)
            print("Query successful executed.")
        except Error as e:
            print("Failed to execute query: {}".format(e))

    def get_value(self):
        value = self.cursor.fetchall()
        return value

    def close(self):
        print("Closing connection to database.")
        try:
            self.cnx.close()
            print("Closed connection to database.")
        except Error as e:
            print("Failed to close connection: {}".format(e))

