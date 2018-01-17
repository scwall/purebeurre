from packages.databases.add_information_function import add_information_connection
from packages.databases.bl_models import CategoriesBL, ProductsBL, ConnectionBL
from packages.databases.databases import Database
from packages.databases.models import Categories, Products, Link_category_product
import os

def change_display_products_and_categories(list_numbers, command):
    if str(command).lower() == "suivant":
        list_numbers[0] = list_numbers[0] + 30
        list_numbers[1] = list_numbers[1] + 30
    if str(command).lower() == "precedent" and list_numbers[0] > 0:
        list_numbers[0] = list_numbers[0] - 30
        list_numbers[1] = list_numbers[1] - 30
    return list_numbers


connection = Database()
if connection.result_connection["error"] is not False:
    add_information_connection()
ConnectionBL.set_connection(connection)

categories_effective = True
products_effective = True
categories_numbers_display = [0, 30]
products_numbers_display = [0, 30]
while categories_effective is True:
    print("bienvenue sur la recherche de bouffe")
    print("ceci est un test")
    print("premiere page")
    list_categories = CategoriesBL.get_categories_numbers(*categories_numbers_display)
    for category in list_categories:
        print(category.id, category.name)
    print("entrer 'suivant' pour passer à la page suivante \n " 
          "entrer 'précédent' pour revenir à la page précédente \n"
          "pour selectionner une catégorie, indiquer juste le numéro de la categorie")

    command = input("> ")
    categories_numbers_display = \
        change_display_products_and_categories(categories_numbers_display, command)

    if command.isdigit() and int(command) >= categories_numbers_display[0] and int(command) <= categories_numbers_display[1]:
        list_number_id_product = []
        category_id = command
        while products_effective is True:
            products = ProductsBL.get_product_on_category(category_id, *products_numbers_display)
            print("Voici la liste des produits de la catégorie " + ' " ' + str(
                CategoriesBL.get_categorie_id(category_id).name) + ' " ')

            for product in products:
                list_number_id_product.append(product.id)
                print(product.id, " ", product.name)

            print("entrer 'suivant' pour passer à la page suivante \n "
                  "entrer 'précédent' pour revenir à la page précédente \n"
                  "pour selectionner un produit, indiquer juste le numéro du produit")
            command = input("> ")
            products_numbers_display = change_display_products_and_categories(products_numbers_display,command)
            if command.isdigit() and int(command) >= list_number_id_product[0] and int(command) <= list_number_id_product[len(list_number_id_product)-1] :
                print("Nom du produit " + ProductsBL.get_product_id(int(command)).name)
                print("Description du produit " + ProductsBL.get_product_id(int(command)).description)
                print("Grade de nutrition " + ProductsBL.get_product_id(int(command)).nutrition_grade)
                print("lien https du produit " + ProductsBL.get_product_id(int(command)).link_http)
            command = input("Voulez vous trouver des  meilleurs alternatives \n"
                            "dans cette catégorie à votre produit ?")
            if command.lower() == "oui":
                test =  ProductsBL.get_product_best_grade(category_id)
                for test in test:
                    print(test.name)



