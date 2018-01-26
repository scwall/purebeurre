import os
from pathlib import Path
import sqlalchemy

def cls():
   os.system('cls' if os.name == 'nt' else 'clear')


def percentage_calculation(count, total_count):
    return int(100 * (count / total_count))


def road_os_path(*roadfile, level=1):
    return os.path.join(str(Path(__file__).parents[level]), *roadfile)

def change_display_products_and_categories(list_numbers, command):
    if str(command).lower() == "!>":
        list_numbers[0] = list_numbers[0] + 30
        list_numbers[1] = list_numbers[1] + 30
    if str(command).lower() == "!<" and list_numbers[0] > 0:
        list_numbers[0] = list_numbers[0] - 30
        list_numbers[1] = list_numbers[1] - 30
    return list_numbers

def product_display(list_product_dic,command):
      print("Nom du produit : {name_product} \n "
          "Description du produit: {product_description} \n "
          "Grade de nutrition: {nutrition_grade} \n"
          "Lien https du produit: {link_http}".format(
        name_product=list_product_dic[int(command)].name,
        product_description=list_product_dic[int(command)].description,
        nutrition_grade=list_product_dic[int(command)].nutrition_grade,
        link_http=list_product_dic[int(command)].link_http))
      return
def print_how_to_use(type):
    if type == "category":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"""
              "entrer '!# pour revenir au menu précédent"
              "pour sélectionner une catégorie, indiquer juste le numéro de la categorie")
    if type == "product":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"""
              "pour revenir en arrière entrer !#"
              "pour selectionner un produit, indiquer juste le numéro du produit")
    if type == "save":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"
              "pour sélectionner un produit sauvegarder, indiquer juste le numéro du produit ")



