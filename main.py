import pymysql
import json
from packages.recovery.recovery import recovery
from packages.road_os_path import road_os_path

with open(road_os_path("packages","connection_databases.json")) as f:
    info_connection = json.load(f)
connection = ""
try:
    connection = pymysql.connect( host= info_connection['host'],
                                 user=info_connection['user'],
                                 password=info_connection['password'],
                                 db=info_connection['db'],
                                 charset=info_connection['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
except:
    connection_complete = True
    while connection_complete is True :
        print("connection unsuccessful!!")

        with open(road_os_path("packages", "connection_databases.json"),'w') as f:
           info_connection = {}
           info_connection["host"] = input("enter the hostname of the databases: ")
           info_connection["user"] = input("enter the username of the databases: ")
           info_connection["password"] = input("enter the password of the databases: ")
           info_connection["db"] = input("enter the db name of the databases: ")
           info_connection["charset"] = str(input("enter the charstet used (defaut=utf8): ") or "utf8mb4")
           f.write(json.dumps(info_connection,indent=2))
        try:
            connection = pymysql.connect( host= info_connection['host'],
                                         user=info_connection['user'],
                                         password=info_connection['password'],
                                         db=info_connection['db'],
                                         charset=info_connection['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)
            connection_complete = False
        except:
            pass

cursor = connection.cursor()
cursor.execute("SELECT COUNT(DISTINCT `name`) FROM `Products`")
number_products = cursor.fetchone()

if number_products['COUNT(DISTINCT `name`)'] != 0:
    recovery(cursor,connection)

