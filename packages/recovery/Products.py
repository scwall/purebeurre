class Products:
    def __init__(self, cursor, connection, name, description, nutrition_grade, shop, link_http):
        self.cursor = cursor
        self.connection = connection
        self.name = name
        self.description = description
        self.nutrition_grade = nutrition_grade
        self.shop = shop
        self.link_http = link_http

    def insert_databases(self):
        """

        ret
        :return:
        """
        sql = "INSERT INTO `Products` (`name`,`description`,`nutrition_grade`,`shop`,`link_http`) VALUES (%s, %s, %s, %s, %s) "
        self.cursor.execute(sql, (self.name, self.description, self.nutrition_grade, self.shop, self.link_http))
        self.connection.commit()
