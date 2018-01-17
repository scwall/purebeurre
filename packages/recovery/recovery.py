# coding: utf8
from multiprocessing import Pool

import multiprocessing
import requests

from packages.databases.bl_models import CategoriesBL, ProductsBL, ConnectionBL
from packages.databases.models import Categories, Products, Link_category_product
from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database

# from packages.products import Products
# from packages.link_categories_products import Link_category_product
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
ConnectionBL.set_connection(connection)
# for categories in categories_dic['tags']:
#     if int(categories['products']) > 10 or str(categories['name']).lower() != str(categories['id']).lower():
#         categories_add = Categories(name=categories['name'], link_http=categories['url'], id_category=categories['id'])
#         connection.connect.add(categories_add)
#
# connection.connect.commit()

#
categories_all = CategoriesBL.get_categories()
connection.connect.expunge_all()
# recovery the products
number_page = 1
final_page = True
while final_page is True:
    products_dic = url_request("https://fr.openfoodfacts.org", number_page)
    if not products_dic['products']:
        final_page = False
    for product in products_dic["products"]:
        if 'nutrition_grades' in product.keys() \
                and 'product_name_fr' in product.keys() \
                and 'categories_tags' in product.keys() \
                and len(product['product_name_fr']) >= 1 \
                and len(product['product_name_fr']) <= 100:
            try:
                article = Products(name=product['product_name_fr'], description=product['ingredients_text_fr'],
                                   nutrition_grade=product['nutrition_grades'], shop=product['stores'],
                                   link_http=product['url'],
                                   categories=CategoriesBL.get_categories_by_tags(product['categories_tags']))
            except KeyError:
                continue

            connection.connect.add(article)
            connection.connect.commit()
    print(number_page)
    number_page += 1
connection.connect.commit()
