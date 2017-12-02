import pickle

import pymysql

from packages.road_os_path import road_os_path


class Database:
    def __init__(self):

        self._result_connection = {"error": ""}
        self.file = open(road_os_path("packages", "databases", "database_info"), 'br')

        self.info_connection = pickle.Unpickler(self.file)
        try:
            self.info_connection = self.info_connection.load()
            self.file.close()
        except:
            self.file.close()
            self._result_connection["error"] = "first"

        if self._result_connection["error"] != "first":
            self.host = self.info_connection["host"]
            self.user = self.info_connection["user"]
            self.password = self.info_connection["password"]
            self.db = self.info_connection["db"]
            self.charset = self.info_connection["charset"]
            self.port = self.info_connection["port"]
            self.connection()
            self.connection.close()

    def connection(self):
        try:

            self.connection = pymysql.connect(host=self.host,
                                              user=self.user,
                                              password=self.password,
                                              db=self.db,
                                              charset=self.charset,
                                              port=self.port,
                                              cursorclass=pymysql.cursors.DictCursor)
            self._result_connection["error"] = False
            return (self.connection)
        except pymysql.err.MySQLError as exception:
            if str(exception)[1:5] == str(1045):
                self._result_connection["error"] = "password"
            if str(exception)[1:5] == str(1698):
                self._result_connection["error"] = "username"
            if str(exception)[1:5] == str(1044):
                self._result_connection["error"] = "database"
            if str(exception)[1:5] == str(2003):
                self._result_connection["error"] = "hostname or password"

    def _get_result_connection(self):

        return self._result_connection

    def add_parameter(self, dic_parameter):
        self.file = open(road_os_path("packages", "databases", "database_info"), 'bw')
        self.info_connection = {}
        if "host" in dic_parameter:
            self.host = dic_parameter["host"]
        if "user" in dic_parameter:
            self.user = dic_parameter["user"]
        if "password" in dic_parameter:
            self.password = dic_parameter["password"]
        if "db" in dic_parameter:
            self.db = dic_parameter["db"]
        if "charset" in dic_parameter:
            self.charset = dic_parameter["charset"]
        if "port" in dic_parameter:
            self.port = dic_parameter["port"]
        self.info_connection = {"host": self.host, "user": self.user, "password": self.password, "db": self.db,
                                "charset": self.charset,
                                "port": self.port}
        self.connection()
        add_info_connection = pickle.Pickler(self.file)
        add_info_connection.dump(self.info_connection)
        self.file.close()

    def insert_databases(self, insert):
        connection = self.connection()
        cursor = connection.cursor()

        column = ("".join(insert.keys()))
        cursor.execute(
            "INSERT INTO " + str("".join(insert.keys())) + str(",".join(insert[column].keys())) + " VALUES " + str(
                ",".join(insert[column].values())))
        self.connection.commit()
        self.connection.close()

    def select_databases(self, insert):
        connection = self.connection()
        cursor = connection.cursor()

        column = ("".join(insert.keys()))
        cursor.execute(
            "SELECT " + str(",".join(insert[column].values())) + " FROM " + str("".join(insert.keys())))
        self.connection.commit()
        self.connection.close()
