import os
from pathlib import Path
import pip
import os
import sys



def install_all_packages(modules_to_try):

    for module in modules_to_try:
        try:
           __import__(module)
        except ImportError as e:
            import os
            euid = os.geteuid()
            if  (lambda major, minor: major == 3 and minor >= 5)(sys.version_info.major, sys.version_info.minor) is False:
                sys.exit('Vous utiliser une mauvaise version de python, version demandée python >= 3.5')
            elif euid != 0:
                root = True
                while root is True:
                    print("Il manque certaines librairies pour executer le programme, vous devez le relancer \n"
                          " en root pour que pip puisse les installer, si vous utilisez un environment virtuel (virtualenv)\n"
                          "Confirmer par !1 sinon !0")
                    command = input("> ")
                    if command == "!1":
                        pip.main(['install', module])
                        root = False
                    if command == "!0":
                        sys.exit("Veillez relancer le programme en root")
            else:
                pip.main(['install',module])


def clr():
    os.system('clr' if os.name == 'nt' else 'clear')


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


def product_display(list_product_dic, command):
    print("Nom du produit : {name_product} \n "
          "Description du produit: {product_description} \n "
          "Grade de nutrition: {nutrition_grade} \n"
          "Lien https du produit: {link_http}".format(name_product=list_product_dic[int(command)].name,
                                                      product_description=list_product_dic[int(command)].description,
                                                      nutrition_grade=list_product_dic[int(command)].nutrition_grade,
                                                      link_http=list_product_dic[int(command)].link_http))


def print_how_to_use(type):
    if type == "category":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"
              "entrer '!# pour revenir au menu précédent\n"
              "entrer '!@' pour quitter l'application\n"
              "pour sélectionner une catégorie, indiquer juste le numéro de la categorie")
    if type == "product":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"
              "pour revenir en arrière entrer !#\n"
              "entrer '!@' pour quitter l'application\n"
              "pour selectionner un produit, indiquer juste le numéro du produit \n")
    if type == "save":
        print("entrer '!>' pour passer à la page suivante \n "
              "entrer '!<' pour revenir à la page précédente \n"
              "pour sélectionner un produit sauvegarder, indiquer juste le numéro du produit \n")
