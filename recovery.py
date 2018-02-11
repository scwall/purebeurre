try:
    import sys
    import requests
    import time
    from packages.functions import clr, percentage_calculation, install_all_packages
    from packages.databases.add_information_function import add_information_connection
    from packages.databases.databases import Database
    from packages.databases.models import Categories, Products
    from packages.databases.query_models import CategoriesQuery, ConnectionQuery, ProductsQuery

except:
    install_all_packages(['requests', 'sqlalchemy', 'pymysql'])
    sys.exit('Veuillez relancer recovery.py')
if (lambda major, minor: major == 3 and minor >= 5)(sys.version_info.major,
                                                    sys.version_info.minor) is False:
    sys.exit('Vous utilisez une mauvaise version de python, version demandée python >= 3.5')
command_list = ["!1", "!0"]
print("Bienvenue dans la récupération des données du site openfoodfact\n"
      "la récupération des catégories et des produits peut prendre plusieurs heures\n"
      "veuillez ne pas éteindre votre ordinateur pendant la récupération\n"
      "Souhaitez-vous récupérer les données oui : !1 non: !0 ?\n"
      )
command = input("> ")
if command.lower() == "!1":
    clr()
    print("Connexion à la base de données")
    connection = Database()
    if connection.result_connection["error"] is not False:
        add_information_connection()
    connection = Database()
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
    already_saved_products = ProductsQuery.get_products_count()
    if already_saved_categories > 1:
        already_saved_boucle = True
        while already_saved_boucle is True:
            print("Vous semblez avoir déjà récupéré les données sur openfoodfact\n"
                  "il y a actuellement " + str(already_saved_categories) + " Categories et " + str(
                already_saved_products) + " produits dans votre base de données")
            print(
                "Si l'application à planté ou qu'il y a eu une erreur et que vous voulez ré-éxecuter la récupération\n"
                "veuillez confirmer par '!1' Pour recommencer depuis le début ou '!0' pour annuler\n")

            command = input("> ")
            if command == '!1':
                connection.connect.close()
                connection.drop_table()
                connection.create_table()
                already_saved_boucle = False

            if command == '!0':
                sys.exit("Annulation")
            if command.isdigit() is False and command not in command_list:
                print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
                time.sleep(2)

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

            print("Récuperation des produits, ", percentage_calculation(count, total_count), "%", " d'effectué(s)",
                  end='\r')
            sys.stdout.flush()
            count += 1
        number_page += 1
    connection.connect.commit()

    print("Récupération des produits réussis\n"""
          "vous avez récupéré la totalité des produits et catégories\n"
          "vous pouvez utiliser le programme principal"
          )

if command == "!0":
    sys.exit("Récupération annulée")
if command.isdigit() is False and command not in command_list:
    print("Vous avez inséré un caractère illégal,veuillez insérer un chiffre ou une commande")
    time.sleep(2)
