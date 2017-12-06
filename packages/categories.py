import requests

from packages.databases.databases import Database
from packages.search_quote import search_quote


class Categories:
    """
    Go get the categories with the link that is retrieved in url. it will then connect to the database and insert the
    data The result will be tested to see if it does not contain quotation marks, if so it will transform the text
    into a list to add a double quote, this will allow the sql request not to crash. :categories_dic: will retrieve
    in the variable the json file transformed into a dictionary

    """

    def recovery(self, url):
        self.url = url
        self.dic = {"Categories": {}}
        r = requests.get(url)
        categories_dic = r.json()
        connection = Database()
        connection.connect_databases()
        for categories in categories_dic['tags']:
            self.dic['Categories']['name'] = search_quote(categories['name'])
            self.dic['Categories']['link_http'] = str("'") + categories['url'] + str("'")
            column = (str("".join(self.dic.keys())))
            format_sql_command = (
                "INSERT INTO {0} ({1}) VALUES ({2})".format(str("".join(self.dic.keys())), str(
                    ",".join(self.dic[column].keys())), str(
                    ",".join(self.dic[column].values()))))
            connection.insert_databases(format_sql_command)
        connection.close_databases()
