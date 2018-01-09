# coding: utf8
from multiprocessing import Pool

import multiprocessing
import requests

from packages.databases.models import Categories, Products, Link_category_product
from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database
# from packages.products import Products
# from packages.link_categories_products import Link_category_product
connection = Database()

if connection.result_connection["error"] is not False:
    add_information_connection()

def tags(object_categories, categories_tags):
    categories_add = []
    for tag in categories_tags:
        for category in object_categories:
            if category.id_category == tag:
                categories_add.append(category)
    return categories_add


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

for categories in categories_dic['tags']:
    if int(categories['products']) > 10 or str(categories['name']).lower() != str(categories['id']).lower():
        categories_add = Categories(name=categories['name'], link_http=categories['url'], id_category=categories['id'])
        connection.connect.add(categories_add)

connection.connect.commit()

categories_all = connection.select_databases(Categories, "all")
connection.connect.expunge_all()
# recovery the products
number_page = 1
final_page = True
while final_page is True:
    products_dic = url_request("https://fr.openfoodfacts.org", number_page)
    if not products_dic['products']:
        final_page = False
    for product in products_dic["products"]:
        if 'nutrition_grades' in product.keys() and 'product_name_fr'  in product.keys() and 'categories_tags' in product.keys():
            try:
                article = Products(name=product['product_name_fr'], description=product['ingredients_text_fr'],
                                   nutrition_grade=product['nutrition_grades'], shop=product['stores'],
                                   link_http=product['url'])
            except KeyError:
                continue
            pool = Pool(multiprocessing.cpu_count())
            results = pool.starmap(tags, [(categories_all, product['categories_tags'])])
            print(product['categories_tags'])
            pool.close()
            pool.join()

            for result in results[0]:

                article.add_category.append(result)
            local_object = connection.connect.merge(article)
            connection.connect.add(local_object)
            # for tag in product['categories_tags']:
            #     for category in categories_all:
            #         if category.id_category == tag:
            #             article.add_category.append(category)
            # connection.connect.add(article)
            # link id products and id categories

    print(number_page)
    number_page += 1
connection.connect.commit()
