from packages.databases.databases import Database


def add_information_connection():
    """
    :connect_databases: Creation of databases object with connect_databases test
    :info_connection: Creation of the dictionary which will retrieve the parameters for the connect_databases to the database
    :return: Returns that the connect_databases has been successfully established to the database
    """
    info_connection = {}
    connection = Database()
    while connection.result_connection["error"] != False:

        if connection.result_connection["error"] == "hostname or password" or connection.result_connection[
            "error"] == "first":
            info_connection["host"] = input("enter the hostname of the databases: ")
        if connection.result_connection["error"] == "username" or connection.result_connection["error"] == "first":
            info_connection["user"] = input("enter the username of the databases: ")
        if connection.result_connection["error"] == "password" or connection.result_connection["error"] == "first":
            info_connection["password"] = input("enter the password of the databases: ")
        if connection.result_connection["error"] == "database" or connection.result_connection["error"] == "first":
            info_connection["db"] = input("enter the db name of the databases: ")
        if connection.result_connection["error"] == "first":
            info_connection["charset"] = str(input("enter the charset used (default=utf8): ") or "utf8mb4")
        if connection.result_connection["error"] == "hostname or password" or connection.result_connection[
            "error"] == "first":
            info_connection["port"] = int(input("enter the port used (default=3306): ") or 3306)
        connection.add_parameter(info_connection)
    return "connect_databases established"
