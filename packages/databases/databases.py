# coding: utf8
import pickle

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from packages.databases import base
from packages.functions import road_os_path


class Database():
    """
    During the creation of the object there will be a test to know if the database exists or if it must be created.
    if it doesn't exist it will return a string with the answer "first". Otherwise it will open and a test to the
    database with the parameters will be launched, to see if they are correct.
    """

    def __init__(self):

        """

        :file: opens the "database_info" file in binary and read mode and creates the object "file".
        :info_connection: "UnPickler" reconstructs the recovered object in the file file which is in bytes
        :try:   Will test if the object "info_connection" does not return an error during loading.
                If, for example,the initial file is empty
        :except: If this one fails then, it is considered that the file never had any data.
        :host,user,password,db,charset,port:    will retrieve the values of each key,
                                                stored in the dictionary info_connections

        """
        self.result_connection = {"error": ""}
        self.file = open(road_os_path("packages", "databases", "database_info"), 'br')

        self.info_connection = pickle.Unpickler(self.file)
        try:
            self.info_connection = self.info_connection.load()
            self.file.close()
        except:
            self.file.close()
            self.result_connection["error"] = "first"

        if self.result_connection["error"] != "first":
            self.host = self.info_connection["host"]
            self.user = self.info_connection["user"]
            self.password = self.info_connection["password"]
            self.db = self.info_connection["db"]
            self.charset = self.info_connection["charset"]
            self.port = self.info_connection["port"]
            self.connect_databases()
            self.close_databases()

    def connect_databases(self):
        """
        :connect: pymsql.connect creates the object "connect" for database connect_databases
        :return: Returns a dictionary with the type of error that prevents the connect_databases. Either False if there is no error
        :exception: add string in the dictionary "result_connection" with a value that I get back to give the error type
        :rtype: dict | dict
        """
        try:

            self.connect = pymysql.connect(host=self.host,
                                           user=self.user,
                                           password=self.password,
                                           db=self.db,
                                           charset=self.charset,
                                           port=self.port,
                                           cursorclass=pymysql.cursors.DictCursor)
            self.result_connection["error"] = False
            self.connect.close()
            self.engine = create_engine(
                "mysql+pymysql://{username}:{password}@{host}:{port}/{dbName}?charset=utf8&use_unicode=1"
                    .format(username=self.user, password=self.password, host=self.host, port=self.port, dbName=self.db))
            self.Base = base.Base
            self.Base.metadata.bind = self.engine
            DBSession = sessionmaker(bind=self.engine)
            self.connect = DBSession()
            return (self.connect)
        except pymysql.err.MySQLError as exception:
            if str(exception)[1:5] == str(1045):
                self.result_connection["error"] = "password"
            if str(exception)[1:5] == str(1698):
                self.result_connection["error"] = "username"
            if str(exception)[1:5] == str(1044):
                self.result_connection["error"] = "database"
            if str(exception)[1:5] == str(2003):
                self.result_connection["error"] = "hostname or password"

    @property
    def get_result_connection(self):

        """

        :return: returns the response of the encapsulated connect_databases test
        :rtype: dict
        """
        return self.result_connection

    def add_parameter(self, dic_parameters):
        """

        :param dic_parameters:
        :type dic_parameters:
        :return:
        :rtype:
        """
        self.file = open(road_os_path("packages", "databases", "database_info"), 'bw')
        self.info_connection = {}
        if "host" in dic_parameters:
            self.host = dic_parameters["host"]
        if "user" in dic_parameters:
            self.user = dic_parameters["user"]
        if "password" in dic_parameters:
            self.password = dic_parameters["password"]
        if "db" in dic_parameters:
            self.db = dic_parameters["db"]
        if "charset" in dic_parameters:
            self.charset = dic_parameters["charset"]
        if "port" in dic_parameters:
            self.port = dic_parameters["port"]
        self.info_connection = {"host": self.host, "user": self.user, "password": self.password, "db": self.db,
                                "charset": self.charset,
                                "port": self.port}
        self.connect_databases()
        if self.result_connection["error"] == False:
            add_info_connection = pickle.Pickler(self.file)
            add_info_connection.dump(self.info_connection)
            self.file.close()

    def close_databases(self):
        self.connect.close()


