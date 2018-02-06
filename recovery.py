# coding: utf8
import sys

import requests
import time

from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database
from packages.databases.models import Categories, Products
from packages.databases.query_models import CategoriesQuery, ConnectionQuery
from packages.functions import clr, percentage_calculation


print("Bienvenue dans la récupération des données du site openfoodfact\n"
      "La récupération des catégories et des produits peut prendre plusieurs heures\n"
      "Veuillez ne pas éteindre votre ordinateur pendant la récupération\n"
      "Souhaitez-vous récupérer les données o/n ?\n"
      )
command = input("> ")
if command.lower() == "o":
    clr()
    print("Connexion à la base de données")
    connection = Database()
    if connection.result_connection["error"] is not False:
        add_information_connection()
    print("Connexion à la base de données réussie")
    connection.connect_databases()
    ConnectionQuery.set_connection(connection)
    if False in connection.if_exist_table("categories", "link_category_product", "products", "save_products"):
        print("Vous n'avez pas lancé le script de création de la base de données\n ou une table a été supprimée\n")
        print("Suppression des tables")
        connection.connect.close()
        connection.drop_table()
        print("Création des tables")
        connection.create_table()
    already_saved_categories = CategoriesQuery.get_categories_count()

    if already_saved_categories > 1:
        already_saved_boucle = True
        while already_saved_boucle is True:
            print("vous semblez avoir déjà récupéré les données sur openfoodfact\n "
                  "il y a actuellement " + str(already_saved_categories) + " Categories dans votre base de données")
            print(
                "Si l'application à planté ou qu'il y a eu une erreur "
                "et que vous voulez réexecuter la récupération, "
                "veuillez confirmer par 'OUI' Pour recommencer depuis le début ou 'NON' (en majuscule) pour annuler\n")

            command = input("> ")
            if command == 'OUI':
                connection.connect.close()
                connection.drop_table()
                connection.create_table()
                already_saved_boucle = False

            if command == 'NON':
                sys.exit("Annulation")

    count = 0
    total_count = 0
    print("Connexion au site openfoodfact\n")
    categories_json = requests.get("https://fr.openfoodfacts.org/categories.json")
    print("Connexion réussie au site openfoodfact")
    clr()
    categories_dic = categories_json.json()
    total_count = categories_dic['count']
    for categories in categories_dic['tags']:
        if int(categories['products']) > 10 and len(categories['name']) < 150 and str(
                categories['name']).lower() != str(categories['id']).lower():
            categories_add = Categories(name=categories['name'], link_http=categories['url'],
                                        id_category=categories['id'])
            connection.connect.add(categories_add)
            count += 1

        else:
            count += 1

        print("Récuperation des catégories, ", str(percentage_calculation(count, total_count)), "%",
              " d'effectué(s)", end='\r')
        sys.stdout.flush()

    connection.connect.commit()
    print("Récupération des catégories réussies")
    time.sleep(2)
    clr()
    categories_all = CategoriesQuery.get_categories()
    connection.connect.expunge_all()

    # recovery the products
    print("Récupération des produits", end='\r')
    sys.stdout.flush()
    count = 0
    number_page = 1
    final_page = True

    while final_page is True:
        link_page = (lambda url, number_pages: str(url) + "/" + str(number_pages) + ".json")(
            "https://fr.openfoodfacts.org", number_page)
        products_dic = requests.get(link_page).json()
        if products_dic['count']:
            total_count = products_dic['count']
        if not products_dic['products']:
            final_page = False
        for product in products_dic["products"]:
            if 'nutrition_grades' in product.keys() \
                    and 'product_name_fr' in product.keys() \
                    and 'categories_tags' in product.keys() \
                    and 1 <= len(product['product_name_fr']) <= 100:
                try:
                    article = Products(name=product['product_name_fr'], description=product['ingredients_text_fr'],
                                       nutrition_grade=product['nutrition_grades'], shop=product['stores'],
                                       link_http=product['url'],
                                       categories=CategoriesQuery.get_categories_by_tags(product['categories_tags']))
                    connection.connect.add(article)
                except KeyError:
                    continue

            print("Recuperation des produits, ", percentage_calculation(count, total_count), "%", " d'effectué(s)",
                  end='\r')
            sys.stdout.flush()
            count += 1
        connection.connect.commit()
        number_page += 1
    connection.connect.commit()

    print("Récupération des produits réussi\n"""
          "Vous avez récupéré la totalité des produits et catégories\n"
          "Vous pouvez utiliser le programme principal pour consulter les produits"
          )

else:
    print("Récupération annulée")
