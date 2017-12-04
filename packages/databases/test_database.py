from unittest import TestCase
from packages.databases.databases import Database
connection = Database()
class TestDatabase(TestCase):
    def test_connection(self):
        assert {"error": False} == connection.result_connection

    def test_get_result_connection(self):
        assert {"error": False} == connection.get_result_connection

    def test_add_parameter(self):
        self.fail()

    def test_insert_databases(self):
        self.fail()

    def test_select_databases(self):
        self.fail()

    def test_close_databases(self):
        self.fail()
