from packages.databases.databases import Database
from packages.categories import Categories

class Research_foods():

    def __init__(self):
        self.connection = Database()
        self.categories = ""


    def show_category(self,cmd):

        self.categories = self.connection.select_databases(Categories,cmd)
        return self.categories
