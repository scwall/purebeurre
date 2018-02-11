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
            info_connection["host"] = str(input("entrer l'adresse ip ou le hostname de la base de données: "))
        if connection.result_connection["error"] == "username" or connection.result_connection["error"] == "first":
            info_connection["user"] = input("entrer votre nom d'utilisateur de la base de données: ")
        if connection.result_connection["error"] == "password" or connection.result_connection["error"] == "first":
            info_connection["password"] = input("entrer le password utilisé de la base de données: ")
        if connection.result_connection["error"] == "database" or connection.result_connection["error"] == "first":
            info_connection["db"] = input("enter le nom de la table de la base de données: ")
        if connection.result_connection["error"] == "first":
            info_connection["charset"] = str(input("entrer le charset utilisé par la base de données  (défaut=utf8): ") or "utf8")
        if connection.result_connection["error"] == "hostname or password" or connection.result_connection[
            "error"] == "first":
            info_connection["port"] = int(input("entrer le port utilisé par la base de données (défaut=3306): ") or 3306)
        connection.add_parameter(info_connection)
    print("Connexion à la base de données réussie")
