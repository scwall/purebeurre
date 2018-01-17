from packages.databases.add_information_function import add_information_connection
from packages.databases.databases import Database
from packages.databases.models import Categories,Products,Link_category_product

connection = Database()

effective = True
while effective is True:
    print("bienvenue sur la recherche de bouffe")
    print("ceci est un test")
    print("premiere page")
    list_categories = Categories.get_categories_numbers(connection, 1, 30)
    for category in list_categories:
        print(category.id, category.name)
    print("entrer 'suivant' pour passer à la page suivante \n "
          "pour sauter directement à une page, entrer 'page' et le numéro de la page \n "
          "pour selectionner une catégorie, indiquer juste le numéro de la categorie")

    command = input("> ")


