import requests

from packages.categories import Categories
from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database
from packages.link_categories_products import Link_categories_products
from packages.products import Product

connection = Database()
if connection.result_connection["error"] is not False:
    add_information_connection()


def url_request(url, number):
    """
    :param url: url for modification for the pages
    :type url: str
    :param number: number for the page
    :type number: int
    :return: return json file
    """
    url_number = str(url) + "/" + str(number) + ".json"
    r = requests.get(url_number)
    return r.json()


r = requests.get("https://fr.openfoodfacts.org/categories.json")
categories_dic = r.json()
connection = Database()
connection.connect_databases()

# recovery the categories
for categories in categories_dic['tags']:
    categories_add = Categories(categories['name'], categories['url'], categories['id'])
    connection.insert_databases(categories_add)

# recovery the products
number_page = 1
final_page = True

while final_page is True:
    products_dic = url_request("https://fr.openfoodfacts.org", number_page)
    if not products_dic['products']:
        final_page = False
    for product in products_dic["products"]:
        if 'nutrition_grades' in product.keys() and 'product_name_fr' in product.keys():
            article = Product(product['product_name_fr'], product['ingredients_text_fr'],
                              product['nutrition_grades'], product['stores'], product['url'],
                              product['categories_tags'])
            connection.insert_databases(article)
            # link id products and id categories
            result_id_product = connection.select_databases("Products", ["id"],
                                                            ("WHERE " + "name=" + '"' + article.get_object_structure[
                                                                "name"] + '"'))
            result_id_product = result_id_product["id"]
            for category_tags in article.get_categories_tags:
                result_id_categories = connection.select_databases("Categories", ["id"],
                                                                   (
                                                                       "WHERE " + "id_category=" + '"' + category_tags + '"'))
                result_id_categories = result_id_categories["id"]
                link_categories_products = Link_categories_products(result_id_product, result_id_categories)
                connection.insert_databases(link_categories_products)

    number_page += 1
