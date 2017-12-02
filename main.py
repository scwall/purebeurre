from packages.databases.databases import Database
from packages.recovery.recovery import recovery

connection = Database()
while connection._result_connection["error"] != False:

    info_connection = {}
    if connection._result_connection["error"] == "hostname or password" or connection._result_connection[
        "error"] == "first":
        info_connection["host"] = input("enter the hostname of the databases: ")
    if connection._result_connection["error"] == "username" or connection._result_connection["error"] == "first":
        info_connection["user"] = input("enter the username of the databases: ")
    if connection._result_connection["error"] == "password" or connection._result_connection["error"] == "first":
        info_connection["password"] = input("enter the password of the databases: ")
    if connection._result_connection["error"] == "database" or connection._result_connection["error"] == "first":
        info_connection["db"] = input("enter the db name of the databases: ")
    if connection._result_connection["error"] == "first":
        info_connection["charset"] = str(input("enter the charset used (default=utf8): ") or "utf8mb4")
    if connection._result_connection["error"] == "hostname or password" or connection._result_connection[
        "error"] == "first":
        info_connection["port"] = int(input("enter the port used (default=3306): ") or 3306)
    connection.add_parameter(info_connection)

