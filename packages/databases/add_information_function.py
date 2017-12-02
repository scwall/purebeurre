def add_information_connection(information_connection):
    info_connection = {}
    if information_connection["error"] == "hostname or password" or information_connection["error"] == "first":
        info_connection["host"] = input("enter the hostname of the databases: ")
    if information_connection["error"] == "username" or information_connection["error"] == "first":
        info_connection["user"] = input("enter the username of the databases: ")
    if information_connection["error"] == "password" or information_connection["error"] == "first":
        info_connection["password"] = input("enter the password of the databases: ")
    if information_connection["error"] == "database" or information_connection["error"] == "first":
        info_connection["db"] = input("enter the db name of the databases: ")
    if information_connection["error"] == "first":
        info_connection["charset"] = str(input("enter the charset used (default=utf8): ") or "utf8mb4")
    if information_connection["error"] == "hostname or password" or information_connection["error"] == "first":
        info_connection["port"] = int(input("enter the port used (default=3306): ") or 3306)
    return info_connection
