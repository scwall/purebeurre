import requests

from packages.databases.databases import Database
from packages.search_quote import search_quote


class Products:
    def url_request(self, url, number):
        url_number = str(url) + "/" + str(number) + ".json"
        r = requests.get(url_number)
        return r.json()

    def recovery(self):
        self.dic = {"Products": {}}
        categories_page = 1
        number_categories = 500
        connection = Database()
        connection.connect_databases()

        while categories_page != number_categories:
            number_page = 1
            final_page = True

            url = connection.select_databases(
                "SELECT {0} FROM {1} WHERE id='{2}'".format(str("link_http"), str("Categories"), str(categories_page)))
            print(url["link_http"])
            while final_page is True:
                products_dic = self.url_request(url["link_http"], number_page)
                if not products_dic['products']:
                    final_page = False
                for product in products_dic["products"]:
                    if 'nutrition_grades' in product.keys() and 'product_name_fr' in product.keys():
                        self.dic['Products']['name'] = search_quote(product['product_name_fr'])
                        self.dic['Products']['description'] = search_quote(product['ingredients_text_fr'])
                        self.dic['Products']['nutrition_grade'] = search_quote(product['nutrition_grades'])
                        self.dic['Products']['shop'] = search_quote(product['stores'])
                        self.dic['Products']['link_http'] = search_quote(product['url'])
                        self.dic['Products']['id_categorie'] = search_quote(str(categories_page))
                        column = ("".join(self.dic.keys()))
                        format_sql_command = (
                            "INSERT INTO {0} ({1}) VALUES ({2})".format(str("".join(self.dic.keys())), str(
                                ",".join(self.dic[column].keys())), str(
                                ",".join(self.dic[column].values()))))
                        print(format_sql_command)
                        connection.insert_databases(format_sql_command)
                        self.dic = {"Products": {}}
                number_page += 1
            categories_page += 1
        connection.close_databases()
