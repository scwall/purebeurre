# test if all packages and libraries is installed and test version python

try:
    import time
    import sys
    from packages.functions import change_display_products_and_categories, product_display, print_how_to_use, \
        install_all_packages, clr
    from packages.databases.add_information_function import add_information_connection
    from packages.databases.query_models import CategoriesQuery, ProductsQuery, ConnectionQuery, SaveProductsQuery
    from packages.databases.databases import Database
    from packages.databases.models import SaveProducts
except:
    install_all_packages(['requests', 'sqlalchemy', 'pymysql'])
    sys.exit('Veuillez relancer main.py')
if (lambda major, minor: major == 3 and minor >= 5)(sys.version_info.major,
                                                    sys.version_info.minor) is False:
    sys.exit('Vous utiliser une mauvaise version de python, version demandée python >= 3.5')
# Connection to the database and test if connection connection information is correct
connection = Database()
if connection.result_connection["error"] is not False:
    add_information_connection()
    connection = Database()
ConnectionQuery.set_connection(connection)

main_menu = True

command_list = ["!#", "!>", "!<", "!1", "!0", "!@", ""]
# Test if the tables is exist
if False in connection.if_exist_table("categories", "link_category_product", "products", "save_products"):
    print("Vous n'avez pas utiliser le script de création de la base de données\n")
    print("Veuillez exécuter le script de création de la base de données\n"
          "ou lancer directement le fichier  recovery.py")
    sys.exit("Base de donnée inexistante ")
already_saved_categories = CategoriesQuery.get_categories_count()
already_saved_products = ProductsQuery.get_products_count()
# Test if the tables contain data
if already_saved_categories < 100 or already_saved_products < 100:
    print("Vous n'avez pas récupérer (ou partiellement) les catégories et les produits \n "
          "Veuillez executer le fichier recovery.py")
    sys.exit("Aucune (ou partiellement)  des categories, et produits dans la base de données ")

while main_menu is True:
    clr()
    print("Bienvenue cette application qui va vous permettre de trouver\n"
          "une alternative à un produit sélectionné\n"
          "Chaque produit à un nutriscore de la lettre D à la lettre A, la lettre A étant le meilleur et la lettre D "
          "le moins bon\n "
          "celui-ci sera noté à coté de 'Grade de nutrition'")
    print("Pour consulter les produits et les catégories, '1'")
    print("Pour consulter les produits enregistrer, '2'")
    command = input("> ")
    if command.isdigit() and int(command) == 1:
        clr()
        search_product = True
        categories_numbers_display = [0, 30]
        while search_product is True:
            list_categories = CategoriesQuery.get_categories_numbers(*categories_numbers_display)
            number = 1
            list_categories_dic = {}
            for category in list_categories:
                list_categories_dic[number] = category
                number += 1
            for key_category, object_category in list_categories_dic.items():
                print(key_category, " ", object_category.name)

            print_how_to_use("category")

            command = input("> ")
            categories_numbers_display = \
                change_display_products_and_categories(categories_numbers_display, command)

            if command.isdigit() and 1 <= int(command) <= len(list_categories_dic.keys()):
                clr()
                category_id = list_categories_dic[int(command)].id
                products_effective = True
                products_numbers_display = [0, 30]
                while products_effective is True:
                    temporary_product_save = command
                    temporary_save = 0
                    list_product_dic = {}
                    products = ProductsQuery.get_product_on_category(category_id, *products_numbers_display)
                    print("Voici la liste des produits de la catégorie " + ' " ' + str(
                        CategoriesQuery.get_categorie_id(category_id).name) + ' " ' + "\n")
                    number = 1
                    for product in products:
                        list_product_dic[number] = product
                        number += 1
                    for key_product, object_product in list_product_dic.items():
                        print(key_product, " ", object_product.name)
                    print_how_to_use("product")
                    command = input("> ")
                    clr()
                    products_numbers_display = change_display_products_and_categories(products_numbers_display, command)
                    if command.isdigit() and 1 <= int(command) <= len(list_product_dic.keys()):
                        product_effective = True
                        product_number_temporary = command
                        while product_effective is True:
                            clr()
                            product_display(list_product_dic, product_number_temporary)
                            print_how_to_use('product')
                            print(
                                "Voulez vous trouver des  meilleurs alternatives dans cette catégorie à votre produit "
                                "? !0\n "
                                "ou voulez vous sauvegarder se produit ? !1\n")

                            command = input("> ")
                            if command.lower() == "!1":
                                save = SaveProducts()
                                save.save_product = list_product_dic[int(product_number_temporary)]
                                connection.connect.add(save)
                                connection.connect.commit()
                                print('Produit sauvegardé')
                                time.sleep(0.5)
                                clr()
                            if command.lower() == "!0":
                                clr()
                                product_quality_effective_display = [0, 30]
                                products_quality_effective = True

                                while products_quality_effective is True:
                                    clr()
                                    print("Meilleure alternative au produit " + list_product_dic[
                                        int(product_number_temporary)].name)
                                    list_best_product_dic = {}
                                    best_products = ProductsQuery.get_product_best_grade(category_id,
                                                                                    *product_quality_effective_display)
                                    number = 1
                                    for product in best_products:
                                        list_best_product_dic[number] = product
                                        number += 1

                                    for key_product, object_product in list_best_product_dic.items():
                                        print(key_product, " ", object_product.name)
                                    print_how_to_use("product")
                                    command = input("> ")
                                    products_numbers_display = change_display_products_and_categories(
                                        product_quality_effective_display, command)
                                    clr()
                                    if command.isdigit() and 1 <= int(command) <= len(
                                            list_best_product_dic.keys()):
                                        clr()
                                        product_quality_effective = True
                                        product_quality_effective_temporary = command
                                        while product_quality_effective is True:
                                            product_display(list_best_product_dic, product_quality_effective_temporary)
                                            print_how_to_use('save_product')
                                            print("Voulez vous sauvegarder votre produit ? oui : !1")
                                            command = input("> ")
                                            if command.lower() == "!1":
                                                save = SaveProducts()
                                                save.save_product = list_best_product_dic[
                                                    int(product_quality_effective_temporary)]
                                                connection.connect.add(save)
                                                connection.connect.commit()
                                                print('Produit sauvegardé')
                                                time.sleep(0.5)
                                                clr()
                                            if command == "!#":
                                                product_quality_effective = False
                                                command = ""
                                            if command == "!@":
                                                sys.exit("Programme stoppé")
                                            if command.isdigit() is False and command not in command_list:
                                                print(
                                                    "Vous avez inséré un caractère illégal,veuillez insérer un "
                                                    "chiffre ou une commande")
                                                time.sleep(2)
                                    if command == "!#":
                                        products_quality_effective = False
                                        command = ""
                                    if command == "!@":
                                        sys.exit("Programme stoppé")
                                    if command.isdigit() is False and command not in command_list:
                                        print(
                                            "Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une "
                                            "commande")
                                        time.sleep(2)
                            if command == "!#":
                                product_effective = False
                                command = ""
                            if command == "!@":
                                sys.exit("Programme stoppé")
                            if command.isdigit() is False and command not in command_list:
                                print(
                                    "Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                                time.sleep(2)
                    if command == "!#":
                        products_effective = False
                        command = ""
                    if command == "!@":
                        sys.exit("Programme stoppé")
                    if command.isdigit() is False and command not in command_list:
                        print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                        time.sleep(2)
            if command == "!#":
                search_product = False
                command = ""
            if command == "!@":
                sys.exit("Programme stoppé")
            if command.isdigit() is False and command not in command_list:
                print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                time.sleep(2)

    if command.isdigit() and int(command) == 2:
        save_menu = True
        save_numbers_display = [0, 30]
        while save_menu is True:
            print("Voici vos sauvegardes\n")
            number_save = SaveProductsQuery.get_save_count()
            if number_save == 0:
                print("Vous n'avez pas de sauvegarde !\n" + "\n")
            save_products = ProductsQuery.get_save_product_numbers(*save_numbers_display)
            list_save_product_dic = {}
            number = 1
            for save_product in save_products:
                list_save_product_dic[number] = save_product
                number += 1
            for key_save_product, object_save_product in list_save_product_dic.items():
                print(key_save_product, " ", object_save_product.name)
            print_how_to_use('save')
            command = input("> ")
            if command.isdigit() and 1 <= int(command) <= len(list_save_product_dic.keys()):
                save_product_menu = True
                while save_product_menu is True:
                    clr()
                    product_display(list_save_product_dic, command)
                    print_how_to_use('save_product')
                    command = input("> ")
                    if command == "!#":
                        save_product_menu = False
                        command = ""
                    if command == "!@":
                        sys.exit("Programme stoppé")
                    if command.isdigit() is False and command not in command_list:
                        print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                        time.sleep(2)
            if command == "!#":
                save_menu = False
                command = ""
            if command == "!@":
                sys.exit("Programme stoppé")
            if command.isdigit() is False and command not in command_list:
                print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                time.sleep(2)
    if command.isdigit() is False and command not in command_list:
        print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
        time.sleep(2)
