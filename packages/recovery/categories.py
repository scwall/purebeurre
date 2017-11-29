class Categories:
    def __init__(self, cursor, connection, name):
        self.name = name
        self.cursor = cursor
        self.connection = connection

    def insert_databases(self):
        sql = "INSERT INTO `Categories` (`name`) VALUES (%s) "
        self.cursor.execute(sql, self.name)
        self.connection.commit()
