from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database

connection = Database()
while connection.result_connection["error"] != False:
    connection.add_parameter(add_information_connection(connection.get_result_connection))
