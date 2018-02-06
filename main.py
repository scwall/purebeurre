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
    sys.exit('Veuillez relancer recovery.py')

connection = Database()
if connection.result_connection["error"] is not False:
    add_information_connection()
ConnectionQuery.set_connection(connection)
search_product = True
main_menu = True
save_menu = True
recovery = True
products_effective = True
products_quality_effective = True
save_product_menu = True
categories_numbers_display = [0, 30]
products_numbers_display = [0, 30]
save_numbers_display = [0, 30]
command_list = ["!#", "!>", "!<", "!1", "!0", "!@"]
if False in connection.if_exist_table("categories", "link_category_product", "products", "save_products"):
    print("Vous n'avez pas utiliser le script de création de la base de données\n")
    print("Veuillez exécuter le script de création de la base de données\n"
          "ou lancer directement le fichier  recovery.py")
    sys.exit("Base de donnée inexistante ")
already_saved_categories = CategoriesQuery.get_categories_count()
already_saved_products = ProductsQuery.get_products_count()
if already_saved_categories < 100 or already_saved_products < 100:
    print("Vous n'avez pas récupérer (ou partiellement) les catégories et les produits \n "
          "Veuillez executer le fichier recovery.py")
    sys.exit("Aucune (ou partiellement)  des categories, et produits dans la base de données ")

while main_menu is True:

    print("Bienvenue cette application qui va vous permettre de trouver\n"
          "une alternative à un produit sélectionné")
    print("Pour consulter les produits et les catégories indiqué '1'")
    print("Pour consulter les produits enregistrer '2'")
    command = input("> ")
    if command.isdigit() and int(command) == 1:
        clr()
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
                while products_effective is True:
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
                        product_display(list_product_dic, command)
                        print_how_to_use('product')
                        print(
                            "Voulez vous trouver des  meilleurs alternatives dans cette catégorie à votre produit ? "
                            "oui :!1 / non: !0\n "
                            "ou voulez vous sauvegarder se produit ? oui !3\n")
                        temporary_save = command
                        command = input("> ")
                    if command.lower() == "!3":
                        save = SaveProducts()
                        save.save_product = list_product_dic[int(temporary_save)]
                        connection.connect.add(save)
                        connection.connect.commit()
                        print('Produit sauvegardé')
                        time.sleep(0.5)
                        clr()
                    if command.lower() == "!1":
                        number = 1
                        list_best_product_dic = {}
                        best_products = ProductsQuery.get_product_best_grade(category_id)
                        for product in best_products:
                            list_best_product_dic[number] = product
                            number += 1

                        while products_quality_effective is True:
                            for key_product, object_product in list_best_product_dic.items():
                                print(key_product, " ", object_product.name)
                            print("Selectionner votre produit")
                            command = input("> ")
                            clr()
                            if command.isdigit() and 1 <= int(command) <= len(
                                    list_best_product_dic.keys()):
                                product_display(list_best_product_dic, command)
                                print_how_to_use('product' + "\n")
                                print("Voulez vous sauvegarder votre produit ? oui : !1/ non : !0")
                                command_save = input("> ")
                                if command_save.lower() == "!1":
                                    save = SaveProducts()
                                    save.save_product = list_best_product_dic[int(command)]
                                    connection.connect.add(save)
                                    connection.connect.commit()
                                    print('Produit sauvegardé')
                                    time.sleep(0.5)
                                    clr()
                            if command == "!#":
                                products_quality_effective = False
                            if command == "!@":
                                sys.exit("Programme stoppé")
                    if command == "!#":
                        products_effective = False
                    if command == "!@":
                        sys.exit("Programme stoppé")
            if command == "!#":
                search_product = False
            if command == "!@":
                sys.exit("Programme stoppé")

    if command.isdigit() and int(command) == 2:
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
                while save_product_menu is True:
                    clr()
                    product_display(list_save_product_dic, command)
                    print_how_to_use('save_product')
                    command = input("> ")
                    if command == "!#":
                        save_product_menu= False
                    if command == "!@":
                        sys.exit("Programme stoppé")
            if command == "!#":
                save_menu = False
            if command == "!@":
                sys.exit("Programme stoppé")
    if command.isdigit() is False and command not in command_list:
        print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
        time.sleep(2)
