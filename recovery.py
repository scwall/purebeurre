# coding: utf8
from multiprocessing import Pool

import multiprocessing
import requests
import os
from packages.databases.query_models import CategoriesQuery, ProductsQuery, ConnectionQuery
from packages.databases.models import Categories, Products, Link_category_product
from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database

# from packages.products import Products
# from packages.link_categories_products import Link_category_product
from packages.functions import cls, percentage_calculation

print("Bienvenue dans la récupération des données du site openfoodfact\n"
      "La récupération des catégories et des produits peut prendre plusieurs heures\n"
      "Veuillez ne pas éteindre votre ordinateur pendant la récupération\n"
      "Souhaitez-vous récupérer les données o/n ?\n"
      )
command = input("> ")
if command.lower() == "o":
    cls()
    print("Connexion à la base de données")
    connection = Database()
    if connection.result_connection["error"] is not False:
        add_information_connection()
    print("Connexion à la base de données réussie")

    # def url_request(url, number):
    #     """
    #     :param url: url for modification for the pages
    #     :type url: str
    #     :param number: number for the page
    #     :type number: int
    #     :return: return json file
    #     """
    #     url_number = str(url) + "/" + str(number) + ".json"
    #     r = requests.get(url_number)
    #     return r.json()
    count = 0
    total_count = 0
    print("Début de la récupération des catégories\n"
          "Connexion au site openfoodfact\n"
          )
    categories_json = requests.get("https://fr.openfoodfacts.org/categories.json")
    print("Connexion réussie au site openfoodfact")
    categories_dic = categories_json.json()
    connection.connect_databases()
    ConnectionQuery.set_connection(connection)
    total_count = categories_dic['count']
    for categories in categories_dic['tags']:
        if int(categories['products']) > 10 or str(categories['name']).lower() != str(categories['id']).lower():
            categories_add = Categories(name=categories['name'], link_http=categories['url'], id_category=categories['id'])
            connection.connect.add(categories_add)
            count += 1
        else:
            count += 1
        print("Récuperation des catégories, ", percentage_calculation(count, total_count), "%", " d'effectué(s)")
        cls()
    connection.connect.commit()
    print("Récupération des catégories réussies")
    cls()
    categories_all = CategoriesQuery.get_categories()
    connection.connect.expunge_all()

    # recovery the products
    print("Récupération des produits")
    count = 0
    number_page = 1
    final_page = True

    while final_page is True:
        link_page = (lambda url,number_page: str(url) + "/" + str(number_page) + ".json")("https://fr.openfoodfacts.org", number_page)
        products_dic = requests.get(link_page).json()
        if products_dic['count']:
            total_count = products_dic['count']
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
                                       categories=CategoriesQuery.get_categories_by_tags(product['categories_tags']))
                except KeyError:
                    continue

                connection.connect.add(article)
            count += 1
        cls()
        print("Recuperation des produits, ",percentage_calculation(count,total_count),"%"," d'effectué(s)")

        number_page += 1
    connection.connect.commit()
    print("Récupération des produits réussi\n"""
          "Vous avez récupéré la totalité des produits et catégories\n"
          "Vous pouvez utiliser le programme principal pour consulter les produits"
          )

else:
    print("Récupération annulée")
